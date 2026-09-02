---
name: freshness-corroboration
description: >-
  Audits entity authority, knowledge graph links, and factual freshness. Detects missing sameAs
  declarations (Wikidata, Knowledge Graph), absent dateModified/lastmod sitemaps, and missing
  brand-truth.json machine-readable truth endpoints.
---

# Freshness & Entity Corroboration Skill

Evaluates the authoritative entity grounding and factual freshness of a brand. Addresses **Round 2 Failure Mode 2: Stale / Wrong Facts**.

## Core Verification Areas

1. **`sameAs` Entity Grounding:**
   - Detects presence of `sameAs` array declarations in JSON-LD / Microdata linking domain entities to Wikidata, Wikipedia, Google Knowledge Graph IDs, and Merchant Center IDs.
   - Prevents AI hallucination caused by disconnected domain identities.

2. **Freshness Meta Tags & Sitemap Timestamping:**
   - Validates `<meta property="article:modified_time">`, `dateModified` in Schema.org JSON-LD, and `<lastmod>` tags in XML sitemaps.
   - Inspects HTTP caching and freshness headers (`Last-Modified`, `ETag`, `Cache-Control`).

3. **Machine-Readable Brand Truth Endpoints:**
   - Inspects `/.well-known/brand-truth.json`, `/facts.json`, and `/brand.json`.
   - Verifies whether canonical brand claims, return policies, spec guarantees, and corporate affiliations are machine-verifiable.

## Usage

```bash
python scripts/check_freshness.py --url https://example.com
```

## References

- [Entity Corroboration Checklist](./references/entity_corroboration_checklist.md)

