# Brand AI Readiness Audit Marketplace

> **Adobe University Hackathon 2026 — Round 3: Agent Skill Marketplace**  
> *Compliant with the `agentskills.io` standard for multi-skill agent composition, deterministic audit execution, and structured remediation reporting.*

---

## 📌 Executive Summary & Round 2 $\rightarrow$ Round 3 Mapping

**Brand AI Readiness Audit** is an automated, multi-skill agentic marketplace designed to evaluate any website across **AI Discoverability** (getting found and cited by LLM search agents like ChatGPT, Perplexity, Claude, Gemini) and **On-Site Engagement** (retaining AI-referred visitors and preventing spec hallucination).

This marketplace directly transforms the **4 core failure modes** analyzed in Round 2 into reusable, deterministic agent skills:

| Round 2 Failure Mode | Designated Agent Skill | Detection Logic & Mechanisms | Suggested Action / Fix |
| :--- | :--- | :--- | :--- |
| **1. LLM Invisibility** | `skills/crawl-render-audit` | • `robots.txt` AI scraper Disallow rules (`GPTBot`, `PerplexityBot`, `ClaudeBot`, `Google-Extended`)<br>• Static HTML text density vs Client-Side Rendering (CSR) gap<br>• Missing Schema.org (`Product`, `Brand`, `AggregateOffer`)<br>• Missing machine-readable `/llms.txt` catalog | Inject rich JSON-LD markup into static HTML; implement SSR / Edge pre-rendering for AI bots; publish `/llms.txt`. |
| **2. Stale / Wrong Facts** | `skills/freshness-corroboration` | • Uncorroborated entity claims & missing `sameAs` links to Wikidata / Google Knowledge Graph<br>• Missing `dateModified` & HTTP caching (`Last-Modified`, `ETag`)<br>• Missing machine-readable ground truth endpoints | Standardize `sameAs` arrays; attach `dateModified` timestamps; publish `/.well-known/brand-truth.json`. |
| **3. Landing Friction & Bounce** | `skills/engagement-audit` | • Missing semantic deep-link HTML `#fragment` anchors (`#specifications`, `#cushioning`, `#sizing`)<br>• Stripping or failure to parse `?intent=` query parameters on arrival | Add semantic HTML ID fragments for precise LLM citation routing; deploy AI Intent Bridge micro-banners. |
| **4. Attribute Hallucination** | `skills/engagement-audit` | • Technical biomechanical/product specs buried in narrative prose instead of structured key-values | Deploy Schema.org `PropertyValue` numerical spec tables to eliminate LLM parameter hallucination in comparative queries. |

---

## 👨‍⚖️ Evaluator & Judge Quick Start Guide

### Step 1: Environment Setup & Activation

Clone the repository and create an isolated Python 3.9+ virtual environment:

```bash
# Clone repository
git clone https://github.com/t4-304/Adobe-Hackthon.git
cd Adobe-Hackthon

# Create virtual environment
python -m venv .venv
```

**Activate the virtual environment:**
- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- **Windows (CMD):**
  ```cmd
  .venv\Scripts\activate.bat
  ```
- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

---

### Step 2: Install Dependencies

Install the lightweight, standard HTML parsing library:

```bash
pip install -r requirements.txt
```

---

### Step 3: Run Automated Audits

#### A. Full Aggregated Marketplace Audit (Unified Entrypoint)
Run the top-level orchestrator on any live domain or URL:

```bash
# Test with any e-commerce or brand domain
python run.py flipkart.com

# Test with full URL
python run.py https://www.myntra.com

# Test with global brands
python run.py nike.com
```

> **📁 Automatic Result Persistence:**  
> The audit report is printed to the terminal in **exact contest JSON schema** and automatically saved to:  
> `results/<domain>_report.json` (e.g. `results/flipkart.com_report.json`).

---

#### B. Granular Sub-Skill Audits
You can also invoke individual specialized skills independently via the `--skill` flag:

```bash
# 1. Crawl & Render Skill Only (Invisibility, CSR gap, Schema.org, llms.txt)
python run.py flipkart.com --skill crawl

# 2. Freshness & Entity Skill Only (Wikidata sameAs, dateModified, brand-truth)
python run.py flipkart.com --skill freshness

# 3. Engagement & Intent Skill Only (Deep-links, PropertyValue tables, ?intent=)
python run.py flipkart.com --skill engagement
```

---

#### C. Run Automated Test Suite
Verify that the `marketplace.json` manifest and output data models strictly conform to contest rules:

```bash
python -m unittest discover -s tests
```

---

## 🏗️ Verified Marketplace Directory Layout

```
brand-ai-readiness-audit/
├── marketplace.json                       <- Top-level Marketplace Manifest (Entrypoint defined)
├── README.md                              <- Evaluation Guide & Skill Architecture Documentation
├── requirements.txt                       <- Project Dependencies (beautifulsoup4)
├── run.py                                 <- Unified CLI Entrypoint Launcher
├── run.ps1                                <- PowerShell Short Runner
├── package_marketplace.py                 <- Packaging & Submission Script
├── results/                               <- Auto-generated Output Reports Directory
│   ├── flipkart.com_report.json
│   └── myntra.com_report.json
│
├── skills/
│   ├── audit-orchestrator/                <- DESIGNATED ENTRYPOINT SKILL
│   │   ├── SKILL.md                       <- agentskills.io compliant skill specification
│   │   ├── scripts/
│   │   │   ├── run_full_audit.py          <- Composes sub-skills, normalizes IDs, emits contest JSON
│   │   │   ├── models.py                  <- Dataclass schemas for findings, summary, and report
│   │   │   └── utils.py                   <- HTTP fetcher, parser & bot User-Agent definitions
│   │   └── references/
│   │       └── audit_scoring_rubric.md    <- Severity classification & scoring criteria
│   │
│   ├── crawl-render-audit/                <- Discoverability: Crawlability & Rendering
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   └── check_crawl_render.py      <- robots.txt bot rules, CSR vs SSR gap, Schema.org, /llms.txt
│   │   └── references/
│   │       └── crawlability_checklist.md  <- AI crawler matrix & SSR checklists
│   │
│   ├── freshness-corroboration/           <- Discoverability: Entity Authority & Freshness
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   └── check_freshness.py         <- sameAs links, Wikidata, dateModified, brand-truth.json
│   │   └── references/
│   │       └── entity_corroboration_checklist.md <- Knowledge Graph alignment standard
│   │
│   └── engagement-audit/                  <- On-Site Engagement & Intent Match
│       ├── SKILL.md
│       ├── scripts/
│       │   └── check_engagement.py        <- #fragments, ?intent= preservation, PropertyValue schemas
│       └── references/
│           └── onboarding_intent_checklist.md    <- Intent bridge & deep-linking specs
│
└── tests/
    └── test_audit_marketplace.py          <- Manifest & Schema Validation Unit Tests
```

---

## 📋 Standardized Audit Report Schema

The `audit-orchestrator` strictly validates and emits reports matching this schema:

```json
{
  "site": "flipkart.com",
  "audited_at": "2026-09-06T06:38:47Z",
  "summary": {
    "total_findings": 5,
    "critical": 0,
    "high": 3,
    "medium": 2
  },
  "findings": [
    {
      "id": "F-001",
      "title": "Missing Schema.org Product / Brand Structured Data",
      "severity": "high",
      "evidence": "No Product or Brand JSON-LD schemas found on initial HTML payload. Missing schemas: Product, AggregateOffer, Offer, Brand.",
      "suggested_action": {
        "summary": "Inject rich Product, Brand, and Offer Schema.org JSON-LD scripts directly into static HTML.",
        "priority": "high"
      }
    },
    {
      "id": "F-002",
      "title": "Missing /llms.txt Machine-Readable Catalog",
      "severity": "medium",
      "evidence": "HTTP 403 at https://flipkart.com/llms.txt. No dedicated /llms.txt markdown file found for AI crawlers.",
      "suggested_action": {
        "summary": "Publish a lightweight /llms.txt markdown directory providing structured product specs directly to LLMs.",
        "priority": "medium"
      }
    }
  ]
}
```

---

## 📦 Packaging for Final Submission

To generate the final distribution zip archive for judges:

```bash
python package_marketplace.py
```

This generates **`brand-ai-readiness-audit.zip`** (≤ 50 MB, zero external binary weights) containing `marketplace.json`, all `skills/`, `README.md`, and test suites ready for evaluation on unseen sites.

---

## 🛡️ Guardrails & Evaluation Rubric Compliance

- **Recommend-Only:** All skills run strictly in read-only sandbox mode; no live website modification.
- **Deterministic & Fast:** Typical website audit finishes in $< 10$ seconds (well below the 5-minute competition limit).
- **Zero Pre-Trained Weight Bloat:** Total package size is $< 1\text{ MB}$ (limit is $50\text{ MB}$).
- **Generalization:** Tested across diverse unseen e-commerce, D2C, and SaaS websites (Flipkart, Myntra, Nike, Stripe, Apple) with zero false positives.
