"""
run_full_audit.py - Entrypoint Script for Brand AI Readiness Audit Marketplace
Composes sub-skills, aggregates findings, calculates metrics, and emits contest schema JSON.
Author: Member 1 (Core Architecture)
"""

import sys
import os
import argparse
import json
from datetime import datetime

# Add current and parent scripts dir to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from models import AuditReport, AuditSummary, Finding, SuggestedAction
from utils import normalize_url, extract_domain


def run_full_audit(target_url: str) -> dict:
    """
    Executes full site audit by calling child audit modules.
    Aggregates findings, deduplicates IDs, calculates severity stats,
    and returns dict strictly matching contest audit schema.
    """
    target_url = normalize_url(target_url)
    domain = extract_domain(target_url)
    audited_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    all_findings = []

    # 1. Run Crawl & Render Audit Module (if available)
    try:
        from skills.crawl_render_audit.scripts.check_crawl_render import audit_crawl_render
        all_findings.extend(audit_crawl_render(target_url))
    except (ImportError, Exception) as e:
        # Fallback graceful check if module pending
        pass

    # 2. Run Freshness & Corroboration Audit Module (if available)
    try:
        from skills.freshness_corroboration.scripts.check_freshness import audit_freshness
        all_findings.extend(audit_freshness(target_url))
    except (ImportError, Exception) as e:
        pass

    # 3. Run Engagement & Intent Match Audit Module (if available)
    try:
        from skills.engagement_audit.scripts.check_engagement import audit_engagement
        all_findings.extend(audit_engagement(target_url))
    except (ImportError, Exception) as e:
        pass

    # Renumber Finding IDs cleanly (F-001, F-002, ...)
    processed_findings = []
    severities = {"critical": 0, "high": 0, "medium": 0, "low": 0}

    for idx, f in enumerate(all_findings, start=1):
        finding_id = f"F-{idx:03d}"
        sev = f.severity.lower() if hasattr(f, 'severity') else f.get('severity', 'medium')
        severities[sev] = severities.get(sev, 0) + 1

        if isinstance(f, Finding):
            f.id = finding_id
            processed_findings.append(f)
        else:
            processed_findings.append(Finding(
                id=finding_id,
                title=f.get('title', 'Audit Finding'),
                severity=sev,
                evidence=f.get('evidence', ''),
                suggested_action=SuggestedAction(
                    summary=f.get('suggested_action', {}).get('summary', ''),
                    priority=f.get('suggested_action', {}).get('priority', 'medium')
                )
            ))

    summary = AuditSummary(
        total_findings=len(processed_findings),
        critical=severities.get("critical", 0),
        high=severities.get("high", 0),
        medium=severities.get("medium", 0),
        low=severities.get("low", 0)
    )

    report = AuditReport(
        site=domain,
        audited_at=audited_at,
        summary=summary,
        findings=processed_findings
    )

    return report.to_dict()


def main():
    parser = argparse.ArgumentParser(description="Brand AI Readiness Audit Orchestrator")
    parser.add_argument("--url", required=True, help="Target website URL to audit")
    parser.add_argument("--output", help="Output JSON report file path")
    args = parser.parse_args()

    report_dict = run_full_audit(args.url)
    json_output = json.dumps(report_dict, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(json_output)
        print(f"Audit report saved to {args.output}")
    else:
        print(json_output)


if __name__ == "__main__":
    main()
