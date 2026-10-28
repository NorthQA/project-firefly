#!/usr/bin/env python3
"""Post a PR review to the Discord webhook in $DISCORD_PR_REVIEW_WEBHOOK:
the summary text as the message, the report attached as a .md file.

Usage: python discord_post.py <pr-review-<number>.md> <summary.txt> [--dry-run]
       python discord_post.py --batch <pr-review-summary-<YYYY-MM-DD>.md> <summary.txt> [--dry-run]

--batch posts a multi-PR summary to $DISCORD_PR_SUMMARY_WEBHOOK instead.
A summary over 2000 chars is split into several messages on line boundaries
(code blocks are closed and reopened across the split); the file goes on the last one.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import uuid

LIMIT = 2000  # Discord caps message content at 2000 chars


def multipart(fields, file_name, file_bytes):
    boundary = uuid.uuid4().hex
    out = b""
    for name, value in fields.items():
        out += (f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n'
                f'Content-Type: application/json\r\n\r\n{value}\r\n').encode()
    out += (f'--{boundary}\r\nContent-Disposition: form-data; name="files[0]"; filename="{file_name}"\r\n'
            f'Content-Type: text/markdown\r\n\r\n').encode() + file_bytes + f'\r\n--{boundary}--\r\n'.encode()
    return out, f"multipart/form-data; boundary={boundary}"


def split(text):
    out, cur, fence = [], "", False
    for ln in text.splitlines(keepends=True):
        # keep room to close a fence ("```\n") here and reopen it in the next message
        if cur and len(cur) + len(ln) + 4 > LIMIT:
            out.append(cur + ("```\n" if fence else ""))
            cur = "```\n" if fence else ""
        assert len(cur) + len(ln) + 4 <= LIMIT, "a single line is too long for Discord"
        cur += ln
        if ln.strip().startswith("```"):
            fence = not fence
    if cur.strip():
        out.append(cur)
    return out


def post(url, body, content_type):
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": content_type,
        "User-Agent": "pr-review-agent (claude-code, 1.2)",  # Discord rejects the default urllib UA
    })
    for _ in range(5):
        try:
            urllib.request.urlopen(req, timeout=60)
            return
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise RuntimeError(f"Discord returned {e.code}: {e.read().decode(errors='replace')}")
            time.sleep(float(json.loads(e.read() or b"{}").get("retry_after", 1)))
    raise RuntimeError("Discord rate limit: gave up after 5 tries")


def main():
    args = [a for a in sys.argv[1:] if a not in ("--dry-run", "--batch")]
    dry = "--dry-run" in sys.argv
    batch = "--batch" in sys.argv
    env, pattern = (("DISCORD_PR_SUMMARY_WEBHOOK", r"pr-review-summary-\d{4}-\d{2}-\d{2}(-\d+)?\.md") if batch
                    else ("DISCORD_PR_REVIEW_WEBHOOK", r"pr-review-\d+\.md"))
    if len(args) != 2:
        sys.exit(__doc__)
    report_path, summary_path = args
    name = os.path.basename(report_path)
    if not re.fullmatch(pattern, name):
        sys.exit(f"Report name must match {pattern}, got {name}")
    with open(report_path, "rb") as f:
        report = f.read()
    with open(summary_path, encoding="utf-8") as f:
        summary = f.read().strip()
    if not summary:
        sys.exit("Summary is empty")
    messages = split(summary)
    assert all(len(m) <= LIMIT for m in messages)
    if dry:
        sys.stdout.reconfigure(encoding="utf-8")
        for i, m in enumerate(messages, 1):
            print(f"--- message {i}/{len(messages)} ({len(m)} chars) ---\n{m}")
        print(f"--- attachment on message {len(messages)}: {name} ({len(report)} bytes)")
        return
    url = os.environ.get(env)
    if not url:
        sys.exit(f"{env} is not set")
    for i, m in enumerate(messages):
        # parse: [] stops PR text from pinging @everyone or roles
        payload = {"content": m, "allowed_mentions": {"parse": []}}
        if i == len(messages) - 1:
            payload["attachments"] = [{"id": 0, "filename": name}]
            post(url, *multipart({"payload_json": json.dumps(payload)}, name, report))
        else:
            post(url, json.dumps(payload).encode(), "application/json")
        time.sleep(0.5)
    print(f"Posted {len(messages)} message(s) with {name} attached to Discord")


if __name__ == "__main__":
    main()
