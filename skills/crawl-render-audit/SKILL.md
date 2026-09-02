---
name: crawl-render-audit
description: >-
  Audits AI discoverability, crawlability, and rendering capabilities. Detects robots.txt
  restrictions against AI user-agents, raw HTML vs CSR text density gaps, Schema.org JSON-LD
  coverage, and /llms.txt availability.
---

# Crawl & Render Audit Skill

Evaluates how AI models and LLM search bots discover, fetch, and parse a brand's website. Addresses **Round 2 Failure Mode 1: LLM Invisibility**.

## Core Verification Areas

1. **AI Bot Permissions in `robots.txt`:**
   - Evaluates disallow/allow rules for `GPTBot`, `PerplexityBot`, `ClaudeBot`, `Google-Extended`, `Amazonbot`, `ByteSpider`, `CCBot`.
   - Identifies whether AI scrapers and indexers are blocked from essential product and category paths.

2. **CSR vs SSR Text Density Gap:**
   - Compares raw static HTML word count/content against fully rendered client-side DOM content.
   - Detects if crucial product specs, pricing, and descriptions are trapped inside client-rendered JavaScript bundles (React, Vue, Angular SPA).

3. **Schema.org JSON-LD Completeness:**
   - Validates existence and syntax of `@type: Product`, `Brand`, `Organization`, `AggregateOffer`.
   - Verifies structured attributes (`name`, `description`, `sku`, `gtin`, `offers`, `aggregateRating`).

4. **Semantic AI Endpoints (`/llms.txt`):**
   - Probes `/.well-known/llms.txt`, `/llms.txt`, and markdown catalog feeds.

## Usage

```bash
python scripts/check_crawl_render.py --url https://example.com
```

## References

- [Crawlability Checklist](./references/crawlability_checklist.md)

