class ReportFormatter:
    @staticmethod
    def print_summary(challenge):
        print("\n" + "="*40)
        print(f" 🕷️  SPIDER ANALYSIS REPORT: {challenge.name}")
        print("="*40)
        
        if challenge.detected_type:
            print(f"[!] Detected: {challenge.detected_type} (Confidence: {challenge.confidence})")
        
        if challenge.variables:
            print("\n[+] Extracted Variables:")
            for k, v in challenge.variables.items():
                val = str(v)
                display_val = val if len(val) < 50 else val[:47] + "..."
                print(f"    - {k}: {display_val}")

        if challenge.flag_candidates:
            print("\n[🏁] Potential Flags Found:")
            for flag in challenge.flag_candidates:
                print(f"    - {flag}")

        if challenge.suggestions:
            print("\n[💡] Suggested Strategies:")
            for s in challenge.suggestions:
                print(f"    - {s}")
        
        print("\n" + "="*40 + "\n")
