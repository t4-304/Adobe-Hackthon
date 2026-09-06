import os
import zipfile

def package_marketplace():
    zip_path = "brand-ai-readiness-audit.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("."):
            if ".git" in root or "__pycache__" in root or zip_path in root:
                continue
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, ".")
                zipf.write(filepath, arcname)
    print(f"Marketplace successfully packaged to {zip_path}")

if __name__ == "__main__":
    package_marketplace()
