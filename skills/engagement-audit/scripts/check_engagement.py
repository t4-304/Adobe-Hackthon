"""
check_engagement.py - On-Site Engagement & Intent Match Audit Module
Solves Round 2 Failure Modes 3 & 4: Landing Friction & Spec Hallucination.
Author: Member 3 (Engagement & Validation Suite)
"""

import sys
import os
import argparse
import json
from typing import List, Dict, Any
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "audit-orchestrator", "scripts"))
try:
    from utils import fetch_url, normalize_url, extract_json_ld_schemas
except ImportError:
    pass


def audit_engagement(target_url: str) -> List[Any]:
    findings = []
    target_url = normalize_url(target_url)
    status, raw_html, _ = fetch_url(target_url)

    if status != 200 or not raw_html:
        return findings

    soup = BeautifulSoup(raw_html, 'html.parser')

    # 1. Check Deep-Link ID Fragment Anchors (#specifications, #cushioning, etc.)
    element_ids = set()
    for el in soup.find_all(True):
        if el.has_attr('id'):
            element_ids.add(el['id'])

    target_fragments = {"specifications", "specs", "features", "details", "sizing", "faq"}
    found_fragments = target_fragments.intersection(element_ids)

    if not found_fragments:
        findings.append({
            "title": "Missing Deep-Link HTML Fragment Anchors for AI Citation Routing",
            "severity": "high",
            "evidence": "No semantic ID fragments (#specifications, #features, #details) found for precise LLM citation routing.",
            "suggested_action": {
                "summary": "Add semantic HTML id attributes to key product sections allowing AI assistants to cite granular URL fragments.",
                "priority": "high"
            }
        })

    # 2. Check PropertyValue Technical Spec Schemas
    schemas = extract_json_ld_schemas(raw_html)
    has_property_values = False
    for s in schemas:
        if s.get('@type') == 'PropertyValue' or 'additionalProperty' in s:
            has_property_values = True
            break

    if not has_property_values:
        findings.append({
            "title": "Unstructured Technical Specs & Missing PropertyValue Schemas",
            "severity": "high",
            "evidence": "Product technical specs exist only in unparsed marketing text rather than structured PropertyValue key-value pairs.",
            "suggested_action": {
                "summary": "Inject Schema.org PropertyValue key-value pairs for technical specifications to prevent LLM attribute hallucination.",
                "priority": "high"
            }
        })

    # 3. Check AI Intent Onboarding Micro-Banners
    has_intent_script = "intent" in raw_html.lower() or "referrer" in raw_html.lower()
    if not has_intent_script:
        findings.append({
            "title": "Missing AI Intent Parameter Retention & Onboarding Bridge",
            "severity": "medium",
            "evidence": "Landing page does not parse ?intent= URI query parameters or AI referral headers to tailor dynamic micro-copy.",
            "suggested_action": {
                "summary": "Deploy an AI Intent Bridge script that reads ?intent= query params and dynamically surfaces queried product features.",
                "priority": "medium"
            }
        })

    return findings


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Engagement & Intent Match Audit Module")
    parser.add_argument("--url", required=True, help="Target URL")
    args = parser.parse_args()
    print(json.dumps(audit_engagement(args.url), indent=2))
