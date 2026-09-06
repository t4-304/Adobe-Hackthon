"""
run.py - Lightweight Unified CLI Launcher for Brand AI Readiness Audit Marketplace
Usage:
  python run.py <url_or_domain>                    # Full 4-skill aggregated audit
  python run.py <url_or_domain> --skill crawl      # Crawl & Render skill only
  python run.py <url_or_domain> --skill freshness  # Freshness & Entity skill only
  python run.py <url_or_domain> --skill engagement # Engagement & Intent skill only

Results are automatically formatted, printed, and saved into results/<domain>_report.json.
"""

import sys
import os
import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser(
        description="Brand AI Readiness Audit Launcher",
        usage="python run.py <url> [--skill {all,crawl,freshness,engagement}]"
    )
    parser.add_argument("url", help="Website domain or URL to audit (e.g. flipkart.com or https://www.nike.com)")
    parser.add_argument(
        "--skill", "-s",
        choices=["all", "crawl", "freshness", "engagement"],
        default="all",
        help="Choose specific skill to run (default: all)"
    )
    parser.add_argument("--output", "-o", help="Custom output JSON path", default=None)

    args = parser.parse_args()
    target_url = args.url.strip()
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = "https://" + target_url

    base_dir = os.path.dirname(os.path.abspath(__file__))

    script_map = {
        "all": os.path.join(base_dir, "skills", "audit-orchestrator", "scripts", "run_full_audit.py"),
        "crawl": os.path.join(base_dir, "skills", "crawl-render-audit", "scripts", "check_crawl_render.py"),
        "freshness": os.path.join(base_dir, "skills", "freshness-corroboration", "scripts", "check_freshness.py"),
        "engagement": os.path.join(base_dir, "skills", "engagement-audit", "scripts", "check_engagement.py")
    }

    target_script = script_map[args.skill]
    cmd = [sys.executable, target_script, "--url", target_url]
    if args.output:
        cmd.extend(["--output", args.output])

    subprocess.run(cmd)

if __name__ == "__main__":
    main()
