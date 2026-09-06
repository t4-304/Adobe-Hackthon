import sys
import os
import argparse
import json
from typing import List, Dict, Any

# Ensure parent imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "audit-orchestrator", "scripts"))
try:
    from models import Finding, SuggestedAction
    from utils import fetch_url, normalize_url, extract_raw_text_word_count, extract_json_ld_schemas, BOT_USER_AGENTS
except ImportError:
    pass


def audit_crawl_render(target_url: str) -> List[Any]:
    findings = []
    target_url = normalize_url(target_url)

    # 1. Check robots.txt for AI Bot blocks
    robots_url = target_url.rstrip('/') + '/robots.txt'
    status, robots_txt, _ = fetch_url(robots_url)

    if status == 200 and robots_txt:
        blocked_bots = []
        for bot_name in ["GPTBot", "PerplexityBot", "ClaudeBot", "Google-Extended"]:
            if f"User-agent: {bot_name}" in robots_txt and "Disallow: /" in robots_txt:
                blocked_bots.append(bot_name)

        if blocked_bots:
            findings.append({
                "title": f"AI Crawlers Blocked in robots.txt ({', '.join(blocked_bots)})",
                "severity": "critical",
                "evidence": f"robots.txt at {robots_url} explicitly disallows AI crawlers: {', '.join(blocked_bots)}.",
                "suggested_action": {
                    "summary": "Remove Disallow rules for AI web scrapers in robots.txt to restore AI search indexing.",
                    "priority": "critical"
                }
            })

    # 2. Check Raw Static HTML Text Density (CSR vs SSR Trap)
    status, raw_html, _ = fetch_url(target_url)
    if status == 200 and raw_html:
        word_count = extract_raw_text_word_count(raw_html)
        if word_count < 150:
            findings.append({
                "title": "Low Static Text Density (Client-Side Rendering Gap)",
                "severity": "high",
                "evidence": f"Raw static HTML contains only {word_count} words. Content is rendered via JavaScript, hiding specs from AI search engines.",
                "suggested_action": {
                    "summary": "Implement Server-Side Rendering (SSR) or Edge HTML rewriting for AI bot User-Agents.",
                    "priority": "high"
                }
            })

        # 3. Check Schema.org JSON-LD Presence
        schemas = extract_json_ld_schemas(raw_html)
        found_types = set()
        for s in schemas:
            t = s.get('@type')
            if isinstance(t, str):
                found_types.add(t)
            elif isinstance(t, list):
                found_types.update(t)

        required_schemas = {"Product", "Brand", "Organization", "Offer", "AggregateOffer"}
        missing_schemas = required_schemas - found_types

        if "Product" not in found_types and "Brand" not in found_types:
            findings.append({
                "title": "Missing Schema.org Product / Brand Structured Data",
                "severity": "high",
                "evidence": f"No Product or Brand JSON-LD schemas found on initial HTML payload. Missing schemas: {', '.join(missing_schemas)}.",
                "suggested_action": {
                    "summary": "Inject rich Product, Brand, and Offer Schema.org JSON-LD scripts directly into static HTML.",
                    "priority": "high"
                }
            })

    # 4. Check /llms.txt Endpoint
    llms_url = target_url.rstrip('/') + '/llms.txt'
    llms_status, llms_text, _ = fetch_url(llms_url)
    if llms_status != 200 or len(llms_text.strip()) < 20:
        findings.append({
            "title": "Missing /llms.txt Machine-Readable Catalog",
            "severity": "medium",
            "evidence": f"HTTP {llms_status} at {llms_url}. No dedicated /llms.txt markdown file found for AI crawlers.",
            "suggested_action": {
                "summary": "Publish a lightweight /llms.txt markdown directory providing structured product specs directly to LLMs.",
                "priority": "medium"
            }
        })

    return findings


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl & Render Audit Module")
    parser.add_argument("--url", required=True, help="Target URL")
    args = parser.parse_args()
    print(json.dumps(audit_crawl_render(args.url), indent=2))
