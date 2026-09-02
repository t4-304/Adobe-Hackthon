# Brand AI Readiness Audit

> **Marketplace Architecture, Skills Breakdown & Required Audit Schema**  
> Compliant with the `agentskills.io` standard for AI agent marketplaces and skill composition.

---

## 📌 Project Overview

**Brand AI Readiness Audit** is an automated, multi-skill agentic audit suite designed to evaluate e-commerce and brand websites for LLM discovery, machine readability, factual corroboration, and AI-assisted customer engagement.

Modern generative AI engines (ChatGPT, Perplexity, Claude, Google Gemini) search, index, corroborate, and refer users to brand websites in ways fundamentally distinct from traditional search engines. This suite identifies critical failure modes and emits structured, actionable remediation plans.

---

## 🏗️ Marketplace & Folder Structure

```
brand-ai-readiness-audit/
|-- marketplace.json                       <- Top-level Marketplace Manifest
|-- README.md                              <- Overview & Skill Composition Doc
`-- skills/
    |-- audit-orchestrator/                <- ENTRYPOINT SKILL (Designated Orchestrator)
    |   |-- SKILL.md
    |   |-- scripts/
    |   |   `-- run_full_audit.py          <- Aggregates sub-skills & emits final JSON report
    |   `-- references/
    |       `-- audit_scoring_rubric.md
    |
    |-- crawl-render-audit/                <- Discoverability: Crawlability & Rendering
    |   |-- SKILL.md
    |   |-- scripts/
    |   |   `-- check_crawl_render.py      <- Checks robots.txt, CSR vs SSR, llms.txt, Schema.org
    |   `-- references/
    |       `-- crawlability_checklist.md
    |
    |-- freshness-corroboration/           <- Discoverability: Entity Authority & Freshness
    |   |-- SKILL.md
    |   |-- scripts/
    |   |   `-- check_freshness.py         <- Checks sameAs links, Wikidata, dateModified, brand-truth.json
    |   `-- references/
    |       `-- entity_corroboration_checklist.md
    |
    `-- engagement-audit/                  <- On-Site Engagement & Intent Match
        |-- SKILL.md
        |-- scripts/
        |   `-- check_engagement.py        <- Checks ?intent= preservation, deep-links, PropertyValue spec tables
        `-- references/
            `-- onboarding_intent_checklist.md
```

---

## 🎯 4 Main Skills Breakdown

### 1. `audit-orchestrator` (Designated Entrypoint)
- **Role:** Coordinates child skills (`crawl-render-audit`, `freshness-corroboration`, `engagement-audit`), composes findings, calculates overall severity distribution, and generates the final standardized report.
- **Output:** Emits the mandatory contest JSON schema.

### 2. `crawl-render-audit`
- **Focus:** *Discoverability: Crawlability & Rendering*
- **Solves Failure Mode 1:** **LLM Invisibility**
- **Core Checks:**
  - `robots.txt` AI bots permissions (`GPTBot`, `PerplexityBot`, `ClaudeBot`, `Google-Extended`, etc.).
  - Raw static HTML text vs. Client-Side Rendered (CSR) text density gap.
  - Presence of Schema.org JSON-LD structured data (`Product`, `Brand`, `Organization`, `AggregateOffer`).
  - Availability of `/llms.txt` and semantic markdown catalog endpoints.

### 3. `freshness-corroboration`
- **Focus:** *Discoverability: Entity Authority & Freshness*
- **Solves Failure Mode 2:** **Stale / Wrong Facts**
- **Core Checks:**
  - `sameAs` array declarations linking domain entities to Wikidata, Knowledge Graph, and merchant profiles.
  - `dateModified` meta tags, lastmod XML sitemaps, and HTTP caching headers (`Last-Modified`, `ETag`).
  - Machine-readable brand truth endpoints (e.g., `/.well-known/brand-truth.json`, `/facts.json`).

### 4. `engagement-audit`
- **Focus:** *On-Site Engagement & Intent Match*
- **Solves Failure Modes 3 & 4:** **Landing Friction & Spec Hallucination**
- **Core Checks:**
  - Deep-link fragment preservation (`#specifications`, `#cushioning`, `#battery-life`) and query intent parameters (`?intent=`).
  - Technical biomechanical and product parameters using `PropertyValue` schemas vs. plain marketing text.
  - AI Intent Bridge micro-banners on landing pages to align arriving users with their prompt context.

---

## 📋 Required Audit Report JSON Schema

The `audit-orchestrator` strictly emits reports matching this schema:

```json
{
  "site": "example.com",
  "audited_at": "2026-09-01T13:00:00Z",
  "summary": {
    "total_findings": 5,
    "critical": 1,
    "high": 2,
    "medium": 2
  },
  "findings": [
    {
      "id": "F-001",
      "title": "Client-Side Rendering (CSR) hides product specs from AI crawlers",
      "severity": "critical",
      "evidence": "Raw static HTML contains only 120 words; rendered DOM has 1,400 words. Key specs are invisible to basic AI scrapers.",
      "suggested_action": {
        "summary": "Implement Server-Side Rendering (SSR) or Edge HTML rewriting for AI bot User-Agents.",
        "priority": "critical"
      }
    },
    {
      "id": "F-002",
      "title": "Uncorroborated Brand Entities & Missing sameAs Schema",
      "severity": "high",
      "evidence": "0 sameAs entity links found linking domain to Wikidata or Google Merchant Center.",
      "suggested_action": {
        "summary": "Add sameAs array pointing to authoritative entity nodes and publish /.well-known/brand-truth.json.",
        "priority": "high"
      }
    }
  ]
}
```

---

## 🚀 Quick Start & Usage

### Running via Python Orchestrator

```bash
# Run full aggregated audit for a website
python skills/audit-orchestrator/scripts/run_full_audit.py --url https://example.com --output report.json

# Run individual child skills
python skills/crawl-render-audit/scripts/check_crawl_render.py --url https://example.com
python skills/freshness-corroboration/scripts/check_freshness.py --url https://example.com
python skills/engagement-audit/scripts/check_engagement.py --url https://example.com
```

### Packaging

The entire marketplace can be packaged into `brand-ai-readiness-audit.zip` for marketplace deployment:

```bash
# Package the marketplace
powershell Compress-Archive -Path * -DestinationPath brand-ai-readiness-audit.zip -Force
```

