import os
import zipfile
import argparse
import subprocess
import sys

def package_marketplace(site_name):
    # Remove common URL parts if user passed a full URL
    clean_name = site_name.replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")
    zip_path = f"{clean_name} AI readiness test.zip"
    
    report_file = f"{clean_name}_report.json"
    readme_file = "README.md"
    
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
        print("Error: Could not find audit scripts to run.")
        return
        
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run audit and package results")
    parser.add_argument("--site", help="Website name to audit and package", required=True)
    args = parser.parse_args()
    package_marketplace(args.site)
