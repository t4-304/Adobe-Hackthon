import os
import zipfile
import argparse
import subprocess
import sys

def package_marketplace(site_name=None):
    if site_name:
        # Remove common URL parts if user passed a full URL instead of just name
        clean_name = site_name.replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")
        zip_path = f"{clean_name} AI readiness test.zip"
    else:
        clean_name = None
        zip_path = "AI readiness test.zip"

    if clean_name:
        report_file = f"{clean_name}_report.json"
        readme_file = f"{clean_name}_README.md"

        print(f"Running audit for {clean_name}...")

        script_path = os.path.join("skills", "audit-orchestrator", "scripts", "run_full_audit.py")
        engagement_script = os.path.join("skills", "engagement-audit", "scripts", "check_engagement.py")

        # Attempt to run the full orchestrator
        if os.path.exists(script_path):
            subprocess.run(
                [sys.executable, script_path, "--url", f"https://www.{clean_name}", "--output", report_file],
                check=False
            )
        elif os.path.exists(engagement_script):
            # Fallback to just the engagement script if orchestrator isn't available
            with open(report_file, "w") as f:
                subprocess.run([sys.executable, engagement_script, "--url", f"https://www.{clean_name}"], stdout=f)
        else:
            print("Warning: Could not find audit scripts to run. Packaging codebase instead.")
            clean_name = None  # Fall through to codebase packaging

        if clean_name:
            # Generate a simple README
            with open(readme_file, "w") as f:
                f.write(f"# AI Readiness Test Results for {clean_name}\n\n")
                f.write(f"This archive contains the automated AI Readiness Audit findings for `{clean_name}`.\n\n")
                f.write("## Files Included\n")
                f.write(f"- `{report_file}`: Detailed JSON report containing findings, severities, and suggested actions.\n")

            # Zip only the resulting files (NOT the codebase)
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                if os.path.exists(report_file):
                    zipf.write(report_file)
                if os.path.exists(readme_file):
                    zipf.write(readme_file)

            # Cleanup the temporary files so they don't clutter the directory
            if os.path.exists(report_file):
                os.remove(report_file)
            if os.path.exists(readme_file):
                os.remove(readme_file)

            print(f"Results successfully packaged into '{zip_path}'")
            return

    # Fallback: package the entire codebase (when no site_name or audit scripts not found)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("."):
            if ".git" in root or "__pycache__" in root:
                continue
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, ".")
                # Ignore all zip files so we don't accidentally package previous zips
                if not file.endswith(".zip"):
                    zipf.write(filepath, arcname)
    print(f"Marketplace successfully packaged to {zip_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run audit and package results")
    parser.add_argument("--site", help="Website name to audit and package (optional)", default=None)
    args = parser.parse_args()
    package_marketplace(args.site)
