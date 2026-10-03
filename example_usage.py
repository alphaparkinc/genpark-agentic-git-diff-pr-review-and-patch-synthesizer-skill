"""Example usage for Git Diff PR Review Synthesizer."""
from client import GitDiffPRReviewSynthesizer

if __name__ == "__main__":
    diff = """--- a/config.py
+++ b/config.py
@@ -1,3 +1,3 @@
-import os
+TOKEN = "prod_ghp_1234567890"
"""
    review = GitDiffPRReviewSynthesizer.analyze_diff(diff)
    print("Verdict:", review["verdict"])
    for f in review["findings"]:
        print(f"[{f['severity']}] {f['message']}")
