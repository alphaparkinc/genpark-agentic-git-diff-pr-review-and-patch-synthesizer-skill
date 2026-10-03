"""MCP server for Git Diff PR Review Synthesizer."""
import sys
import json
from client import GitDiffPRReviewSynthesizer

def handle_request(req):
    method = req.get("method")
    if method == "tools/list":
        return {
            "tools": [{
                "name": "analyze_pr_diff",
                "description": "Performs static code review and security audits on unified git diffs",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "raw_diff": {"type": "string"}
                    },
                    "required": ["raw_diff"]
                }
            }]
        }
    elif method == "tools/call":
        params = req.get("params", {})
        if params.get("name") == "analyze_pr_diff":
            diff = params.get("arguments", {}).get("raw_diff", "")
            res = GitDiffPRReviewSynthesizer.analyze_diff(diff)
            return {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
    return {"error": "Method not found"}

if __name__ == "__main__":
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_request(json.loads(line))))
            sys.stdout.flush()
