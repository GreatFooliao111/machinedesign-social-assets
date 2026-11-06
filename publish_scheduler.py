#!/usr/bin/env python3
"""
MachineDesign.ir - Autonomous Instagram Scheduler via Composio MCP & GitHub Actions
Reads queue.json, finds pending posts where scheduled_at <= now, and publishes them via Composio.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone

MCP_URL = "https://connect.composio.dev/mcp"
ACCOUNT_MAP = {
    "machinedesign.ir": {
        "account": "instagram_cist-proto",
        "ig_user_id": "38943645821950667"
    },
    "h.vatan.doust": {
        "account": "instagram_claw-immund",
        "ig_user_id": "29088697370821217"
    }
}

def call_composio_tool(tool_slug, arguments, account_id, api_key):
    """Executes a Composio tool via JSON-RPC SSE endpoint."""
    headers = {
        "x-consumer-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream"
    }
    payload = {
        "jsonrpc": "2.0",
        "id": int(time.time()),
        "method": "tools/call",
        "params": {
            "name": "COMPOSIO_MULTI_EXECUTE_TOOL",
            "arguments": {
                "tools": [
                    {
                        "tool_slug": tool_slug,
                        "arguments": arguments,
                        "account": account_id
                    }
                ]
            }
        }
    }
    
    req = urllib.request.Request(MCP_URL, data=json.dumps(payload).encode("utf-8"), headers=headers)
    with urllib.request.urlopen(req, timeout=120) as resp:
        for line in resp:
            line_str = line.decode("utf-8")
            if line_str.startswith("data:"):
                data_json = json.loads(line_str[5:].strip())
                if "result" in data_json and "content" in data_json["result"]:
                    raw_text = data_json["result"]["content"][0].get("text", "{}")
                    parsed = json.loads(raw_text)
                    if parsed.get("successful") and parsed.get("data", {}).get("results"):
                        res = parsed["data"]["results"][0]
                        if "error" in res and res["error"]:
                            raise RuntimeError(f"Tool error: {res['error']}")
                        return res.get("response_data", {})
                    elif not parsed.get("successful"):
                        err = parsed.get("error") or parsed.get("data", {}).get("results", [{}])[0].get("error")
                        raise RuntimeError(f"Composio execution failed: {err}")
                elif "error" in data_json:
                    raise RuntimeError(f"RPC error: {data_json['error']}")
    raise RuntimeError("No valid response from Composio MCP endpoint")

def publish_single_post(post, api_key):
    """Publishes a single image, video, or reel to Instagram."""
    acc_info = ACCOUNT_MAP.get(post.get("account"))
    if not acc_info:
        raise ValueError(f"Unknown account: {post.get('account')}")
    
    account_slug = acc_info["account"]
    ig_user_id = acc_info["ig_user_id"]
    
    post_type = post.get("type", "image").lower()
    container_args = {
        "ig_user_id": ig_user_id,
        "caption": post.get("caption", "")
    }
    
    if post_type in ["reel", "video"]:
        container_args["video_url"] = post["media_url"]
        container_args["media_type"] = "REELS"
        if "cover_url" in post and post["cover_url"]:
            container_args["cover_url"] = post["cover_url"]
        if "share_to_feed" in post:
            container_args["share_to_feed"] = post["share_to_feed"]
    else:
        container_args["image_url"] = post["media_url"]
    
    print(f"Creating media container for {post['id']} ({post_type})...")
    container_resp = call_composio_tool("INSTAGRAM_POST_IG_USER_MEDIA", container_args, account_slug, api_key)
    creation_id = container_resp.get("id")
    if not creation_id:
        raise RuntimeError(f"Container creation failed, response: {container_resp}")
    
    print(f"Container created with ID: {creation_id}. Waiting for processing...")
    if post_type in ["reel", "video"]:
        time.sleep(30)  # Wait for Meta video transcoding
    else:
        time.sleep(5)
    
    print(f"Publishing container {creation_id}...")
    publish_args = {
        "ig_user_id": ig_user_id,
        "creation_id": str(creation_id),
        "max_wait_seconds": 60
    }
    publish_resp = call_composio_tool("INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH", publish_args, account_slug, api_key)
    published_id = publish_resp.get("id")
    return published_id or str(creation_id)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    queue_path = os.path.join(script_dir, "queue.json")
    
    api_key = os.environ.get("COMPOSIO_API_KEY")
    if not api_key:
        print("ERROR: COMPOSIO_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)
        
    if not os.path.exists(queue_path):
        print(f"Queue file not found at {queue_path}. Nothing to process.")
        sys.exit(0)
        
    with open(queue_path, "r", encoding="utf-8") as f:
        queue = json.load(f)
        
    now = datetime.now(timezone.utc)
    print(f"[{now.isoformat()}] Processing Instagram post queue ({len(queue)} total items)...")
    
    modified = False
    for post in queue:
        if post.get("status") != "pending":
            continue
            
        sched_time_str = post.get("scheduled_at")
        if not sched_time_str:
            continue
            
        try:
            sched_time = datetime.fromisoformat(sched_time_str.replace("Z", "+00:00"))
        except Exception as e:
            print(f"Invalid timestamp in post {post.get('id')}: {sched_time_str} ({e})")
            continue
            
        if sched_time <= now:
            print(f"--> Post {post.get('id')} is due (Scheduled: {sched_time_str}, Current: {now.isoformat()})")
            try:
                published_id = publish_single_post(post, api_key)
                post["status"] = "published"
                post["published_at"] = datetime.now(timezone.utc).isoformat()
                post["media_id"] = published_id
                post.pop("error", None)
                print(f"SUCCESS: Post {post.get('id')} published! (Media ID: {published_id})")
                modified = True
            except Exception as e:
                print(f"FAILED to publish post {post.get('id')}: {e}", file=sys.stderr)
                post["status"] = "failed"
                post["error"] = str(e)
                modified = True
                
    if modified:
        with open(queue_path, "w", encoding="utf-8") as f:
            json.dump(queue, f, ensure_ascii=False, indent=2)
        print("Queue file updated and saved successfully.")
    else:
        print("No pending posts were due in this cycle.")

if __name__ == "__main__":
    main()
