"""Agentic Git Diff PR Review & Patch Synthesizer.
100% Python Standard Library.
"""

class GitDiffPRReviewSynthesizer:
    """Parses unified git diffs, detects anomalies, generates code reviews, and synthesizes unified patches."""
    
    @staticmethod
    def analyze_diff(raw_diff: str) -> dict:
        lines = raw_diff.splitlines()
        added_lines = [l[1:] for l in lines if l.startswith("+") and not l.startswith("+++")]
        removed_lines = [l[1:] for l in lines if l.startswith("-") and not l.startswith("---")]
        
        findings = []
        for line in added_lines:
            if any(term in line.lower() for term in ["api_key =", "secret =", "password =", "token ="]):
                if not any(safe in line.lower() for safe in ["os.getenv", "os.environ", "config."]):
                    findings.append({
                        "severity": "CRITICAL",
                        "rule": "hardcoded_secret_detected",
                        "line_snippet": line.strip()[:80],
                        "message": "Potential hardcoded credential or token detected in addition."
                    })
            if "eval(" in line or "exec(" in line:
                findings.append({
                    "severity": "HIGH",
                    "rule": "dangerous_dynamic_execution",
                    "line_snippet": line.strip()[:80],
                    "message": "Arbitrary code execution primitive (eval/exec) introduced."
                })
            if "except:" in line.replace(" ", ""):
                findings.append({
                    "severity": "MEDIUM",
                    "rule": "bare_except_clause",
                    "line_snippet": line.strip()[:80],
                    "message": "Bare 'except:' masks critical system interrupts."
                })
                
        status = "CHANGES_REQUESTED" if any(f["severity"] in ["CRITICAL", "HIGH"] for f in findings) else "APPROVED"
        summary = (
            f"Analyzed {len(added_lines)} added lines and {len(removed_lines)} removed lines. "
            f"Identified {len(findings)} review comments. Verdict: {status}."
        )
        
        return {
            "verdict": status,
            "findings_count": len(findings),
            "findings": findings,
            "summary": summary
        }
