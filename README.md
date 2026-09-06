# Brand AI Readiness Audit Marketplace

> **Adobe University Hackathon 2026 — Round 3 Submission**  
> Compliant with the `agentskills.io` standard for AI agent marketplaces, multi-skill composition, and automated brand audits.

---

## 📌 Project Overview & Round 2 $\rightarrow$ Round 3 Encoding

**Brand AI Readiness Audit** is an automated, multi-skill agentic audit marketplace designed to evaluate any brand or e-commerce website for LLM discoverability, machine readability, factual corroboration, and AI-driven customer engagement.

It directly encodes the 4 failure modes identified in Round 2 into deterministic, reusable agent skills:

| Failure Mode | Assigned Agent Skill | What it Detects & Resolves |
| :--- | :--- | :--- |
| **1. LLM Invisibility** | `skills/crawl-render-audit` | • `robots.txt` AI scraper Disallow rules (`GPTBot`, `PerplexityBot`, etc.)<br>• Raw static HTML text density vs Client-Side Rendering (CSR) gap<br>• Schema.org structured data (`Product`, `Brand`, `AggregateOffer`)<br>• Machine-readable `/llms.txt` endpoints |
| **2. Stale / Wrong Facts** | `skills/freshness-corroboration` | • `sameAs` entity links pointing to Wikidata / Google Knowledge Graph<br>• `dateModified` in JSON-LD & HTTP `Last-Modified` / `ETag` freshness headers<br>• Standardized `/.well-known/brand-truth.json` ground-truth endpoint |
| **3. Context Friction & Bounce** | `skills/engagement-audit` | • Semantic deep-link HTML `#fragment` anchors (`#specifications`, `#cushioning`)<br>• Preservation of `?intent=` query parameters & AI Intent Bridge banners |
| **4. Attribute Hallucination** | `skills/engagement-audit` | • Unstructured marketing text vs structured `PropertyValue` specification schemas to eliminate LLM parameter hallucinations in comparative prompts |

---

## 👨‍⚖️ Instructions for Judges / Evaluators (How to Run)

### Prerequisites

Ensure Python 3.9+ is installed. Install the single required HTML parsing dependency:

```bash
pip install -r requirements.txt
```

---

### 1. Run Full Aggregated Audit (Shortest & Recommended)

Run the unified `run.py` launcher with any domain or full URL:

```bash
# Example 1: E-commerce audit
python run.py flipkart.com

# Example 2: D2C / Brand audit
python run.py https://www.myntra.com

# Example 3: Global brand audit
python run.py nike.com
```

> **Automatic Result Storage:**  
> The audit report is printed to the terminal in **exact contest JSON schema** and automatically saved to:  
> `results/<domain>_report.json` (e.g. `results/flipkart.com_report.json`).

---

### 2. Run Individual Sub-Skills (Granular Inspection)

You can run individual specialized skills using the `--skill` flag:

```bash
# 1. Crawl & Render Skill Only (Invisibility & CSR Checks)
python run.py flipkart.com --skill crawl

# 2. Freshness & Entity Skill Only (Wikidata sameAs & Brand Truth)
python run.py flipkart.com --skill freshness

# 3. Engagement & Intent Skill Only (Deep-links & PropertyValue Specs)
python run.py flipkart.com --skill engagement
```

---

### 3. Run Automated Unit & Manifest Tests

Validate that the marketplace manifest and output schemas adhere 100% to contest rules:

```bash
python -m unittest discover -s tests
```

---

## 🏗️ Marketplace Architecture & Directory Layout

```
brand-ai-readiness-audit/
|-- marketplace.json                       <- Top-level Marketplace Manifest (Entrypoint defined)
|-- README.md                              <- Evaluation & Skill Architecture Documentation
|-- requirements.txt                       <- Dependencies (beautifulsoup4)
|-- run.py                                 <- Unified CLI Entrypoint Launcher
|-- package_marketplace.py                 <- Marketplace Packaging & Submission Script
|-- results/                               <- Auto-generated Audit Reports Directory
|   |-- flipkart.com_report.json
|   `-- myntra.com_report.json
|
|-- skills/
|   |-- audit-orchestrator/                <- DESIGNATED ENTRYPOINT SKILL
|   |   |-- SKILL.md
|   |   |-- scripts/
|   |   |   |-- run_full_audit.py          <- Composes sub-skills & emits contest JSON
|   |   |   |-- models.py                  <- Strict dataclass models for contest schema
|   |   |   `-- utils.py                   <- HTTP fetcher & schema parsers
|   |   `-- references/
|   |       `-- audit_scoring_rubric.md
|   |
|   |-- crawl-render-audit/                <- Focus: Discoverability & Crawlability
|   |   |-- SKILL.md
|   |   |-- scripts/
|   |   |   `-- check_crawl_render.py      <- robots.txt, CSR density gap, Schema.org, llms.txt
|   |   `-- references/
|   |       `-- crawlability_checklist.md
|   |
|   |-- freshness-corroboration/           <- Focus: Entity Authority & Consensus
|   |   |-- SKILL.md
|   |   |-- scripts/
|   |   |   `-- check_freshness.py         <- sameAs links, Wikidata, dateModified, brand-truth.json
|   |   `-- references/
|   |       `-- entity_corroboration_checklist.md
|   |
|   `-- engagement-audit/                  <- Focus: On-Site Intent & Spec Verification
|       |-- SKILL.md
|       |-- scripts/
|       |   `-- check_engagement.py        <- #fragments, ?intent= preservation, PropertyValue tables
|       `-- references/
|           `-- onboarding_intent_checklist.md
|
`-- tests/
    `-- test_audit_marketplace.py          <- Automated Manifest & Schema Validation Test Suite
```

---

## 📋 Standardized Audit Report Schema

The entrypoint skill strictly emits and validates reports matching this format:

```json
{
  "site": "example.com",
  "audited_at": "2026-09-06T06:27:36Z",
  "summary": {
    "total_findings": 6,
    "critical": 0,
    "high": 3,
    "medium": 3
  },
  "findings": [
    {
      "id": "F-001",
      "title": "Missing Schema.org Product / Brand Structured Data",
      "severity": "high",
      "evidence": "No Product or Brand JSON-LD schemas found on initial HTML payload. Missing schemas: Brand, Product, AggregateOffer, Offer.",
      "suggested_action": {
        "summary": "Inject rich Product, Brand, and Offer Schema.org JSON-LD scripts directly into static HTML.",
        "priority": "high"
      }
    }
  ]
}
```

---

## 📦 Packaging for Final Submission

To package the entire marketplace into a distribution zip archive:

```bash
python package_marketplace.py
```

This generates `AI readiness test.zip` containing `marketplace.json`, all `skills/`, `README.md`, and test suites.
