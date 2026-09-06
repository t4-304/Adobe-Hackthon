import os
import zipfile
import argparse

def package_marketplace(site_name=None):
    if site_name:
        # Remove common URL parts if user passed a full URL instead of just name
        clean_name = site_name.replace("https://", "").replace("http://", "").replace("www.", "").rstrip("/")
        zip_path = f"{clean_name} AI readiness test.zip"
    else:
        zip_path = "AI readiness test.zip"

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
    parser = argparse.ArgumentParser(description="Package marketplace")
    parser.add_argument("--site", help="Website name to append to the zip filename", default=None)
    args = parser.parse_args()
    package_marketplace(args.site)
