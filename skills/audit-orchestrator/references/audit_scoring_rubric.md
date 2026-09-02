# Audit Scoring Rubric & Severity Classification

This reference document defines the severity classifications and scoring criteria used by `audit-orchestrator` to evaluate findings from child audit skills.

---

## Severity Levels

| Severity | Definition | Impact on AI Search & Conversion | Default Remediation Priority |
| :--- | :--- | :--- | :--- |
| **`critical`** | Complete block or total failure in AI discoverability or fundamental specification loss. | AI models cannot crawl content, discard product, or refuse to recommend due to complete invisibility. | `critical` |
| **`high`** | Severe ambiguity, hallucination risk, missing entity links, or broken intent navigation. | AI hallucinates specifications, misquotes facts, or drops users onto unconfigured generic pages. | `high` |
| **`medium`** | Suboptimal machine readability, missing optional standards, or degraded UX on arriving AI traffic. | AI can parse data but with reduced confidence; landing UX lacks intent bridge context. | `medium` |
| **`low`** | Minor optimizations, non-blocking improvements, or advisory suggestions. | Minimal direct ranking or accuracy penalty. | `low` |

---

## Mapping by Audit Dimension

### 1. Crawlability & Rendering (`crawl-render-audit`)
- **Critical:**
  - `robots.txt` disallows major AI crawlers (`GPTBot`, `PerplexityBot`, `ClaudeBot`).
  - Heavy CSR client-side rendering where critical product specs/text are 100% missing from static HTML.
- **High:**
  - Missing core `Schema.org` JSON-LD (`Product`, `Organization`, `AggregateOffer`).
- **Medium:**
  - Missing `/llms.txt` or markdown-optimized catalogs.

### 2. Entity Authority & Freshness (`freshness-corroboration`)
- **High:**
  - Zero `sameAs` entity links pointing to authoritative Knowledge Graph nodes (Wikidata, Google Merchant Center).
  - Stale facts with missing `dateModified` meta tags and absent `lastmod` XML sitemaps.
- **Medium:**
  - Lack of machine-readable `/.well-known/brand-truth.json` or `/facts.json`.

### 3. On-Site Engagement & Intent Match (`engagement-audit`)
- **High:**
  - Loss or stripping of `#specifications` fragment or `?intent=` query parameters on landing pages.
  - Critical spec discrepancies between marketing claims and structured `PropertyValue` tables.
- **Medium:**
  - Absence of AI Intent Bridge micro-banners welcoming AI-referred users with relevant contextual cues.

---

## Summary Metric Calculation

```json
{
  "total_findings": "Count of all findings across all severities",
  "critical": "Count of critical severity findings",
  "high": "Count of high severity findings",
  "medium": "Count of medium severity findings"
}
```

