import sys
import os
import argparse
import json
from typing import List, Dict, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "audit-orchestrator", "scripts"))
try:
    from utils import fetch_url, normalize_url, extract_json_ld_schemas
except ImportError:
    pass


def audit_freshness(target_url: str) -> List[Any]:
    findings = []
    target_url = normalize_url(target_url)
    status, raw_html, headers = fetch_url(target_url)

    if status != 200 or not raw_html:
        return findings

    # 1. Check sameAs Entity Corroboration Links
    schemas = extract_json_ld_schemas(raw_html)
    same_as_links = []
    for s in schemas:
        same = s.get('sameAs', [])
        if isinstance(same, list):
            same_as_links.extend(same)
        elif isinstance(same, str):
            same_as_links.append(same)

    has_authoritative_same_as = any(
        "wikidata.org" in link or "wikipedia.org" in link or "google.com" in link
        for link in same_as_links
    )

    if not has_authoritative_same_as:
        findings.append({
            "title": "Uncorroborated Brand Entities & Missing sameAs Schema Links",
            "severity": "high",
            "evidence": f"Found {len(same_as_links)} sameAs links, but none point to authoritative knowledge graphs (Wikidata, Wikipedia, Google Merchant Center).",
            "suggested_action": {
                "summary": "Add sameAs array in Brand/Organization Schema pointing to Wikidata and Knowledge Graph nodes to force AI fact corroboration.",
                "priority": "high"
            }
        })

    # 2. Check dateModified & Cache Freshness Signals
    has_date_modified = "dateModified" in raw_html or "http-equiv=\"last-modified\"" in raw_html.lower()
    has_cache_headers = "Last-Modified" in headers or "ETag" in headers

    if not has_date_modified and not has_cache_headers:
        findings.append({
            "title": "Missing Factual Freshness & Timestamp Signifiers",
            "severity": "medium",
            "evidence": "No dateModified JSON-LD attribute or HTTP Last-Modified headers detected on product page.",
            "suggested_action": {
                "summary": "Inject dateModified timestamps into Schema.org markup and serve Last-Modified headers to signal factual recency to crawlers.",
                "priority": "medium"
            }
        })

    # 3. Check /.well-known/brand-truth.json Endpoint
    truth_url = target_url.rstrip('/') + '/.well-known/brand-truth.json'
    t_status, t_text, _ = fetch_url(truth_url)
    if t_status != 200 or not t_text.startswith('{'):
        findings.append({
            "title": "Missing Machine-Readable Brand Truth Endpoint (brand-truth.json)",
            "severity": "medium",
            "evidence": f"HTTP {t_status} at {truth_url}. No standardized brand truth JSON endpoint found for scraper consensus.",
            "suggested_action": {
                "summary": "Publish /.well-known/brand-truth.json detailing active 2026 brand entity claims, pricing, and taglines.",
                "priority": "medium"
            }
        })

    return findings


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Freshness & Entity Corroboration Module")
    parser.add_argument("--url", required=True, help="Target URL")
    parser.add_argument("--output", help="Optional output JSON file path", default=None)
    args = parser.parse_args()

    findings = audit_freshness(args.url)
    json_output = json.dumps(findings, indent=2)
    print(json_output)

    # Auto-save to results folder
    clean_domain = args.url.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0].rstrip("/")
    results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "results"))
    os.makedirs(results_dir, exist_ok=True)
    out_file = args.output or os.path.join(results_dir, f"{clean_domain}_freshness_report.json")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(json_output)
    print(f"\n[Saved to {out_file}]")

