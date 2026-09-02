---
name: audit-orchestrator
description: >-
  Designated entrypoint skill for Brand AI Readiness Audit. Coordinates child skills
  (crawl-render-audit, freshness-corroboration, engagement-audit) and emits a standardized
  contest JSON report matching the required schema.
---

# Audit Orchestrator Skill

The **Audit Orchestrator** is the top-level designated entrypoint for the Brand AI Readiness Audit marketplace. It orchestrates sub-skills, aggregates findings across all audit dimensions, classifies findings by severity, and emits the authoritative audit report JSON.

## Workflow

1. **Target Discovery & Domain Normalization:**
   - Parse and sanitize the target URL.
   - Determine baseline protocol (`https://`), domain name, and key sample endpoints (homepage, product page, sitemap).

2. **Execution of Child Audit Skills:**
   - Run `crawl-render-audit` to evaluate robots.txt, rendering (CSR vs SSR), JSON-LD schemas, and `llms.txt`.
   - Run `freshness-corroboration` to inspect `sameAs` entity links, dateModified/sitemaps, and `brand-truth.json`.
   - Run `engagement-audit` to inspect deep-link fragment preservation, query intent parameters, PropertyValue tables, and AI Intent Bridge micro-banners.

3. **Aggregation & Normalization:**
   - Merge all finding objects, assigning sequential IDs (`F-001`, `F-002`, ...).
   - Categorize severities (`critical`, `high`, `medium`, `low`).
   - Compile summary metrics (`total_findings`, `critical`, `high`, `medium`).

4. **Report Generation:**
   - Emit the final JSON report strictly matching the contest schema.

## Invocation

```bash
python scripts/run_full_audit.py --url https://example.com [--output report.json]
```

## References

- [Audit Scoring Rubric](./references/audit_scoring_rubric.md)

