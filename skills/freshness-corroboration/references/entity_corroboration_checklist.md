# Entity Corroboration & Freshness Checklist

This checklist defines standard requirements for grounding brand facts, resolving entity disambiguation, and establishing machine-verifiable truth for AI models.

---

## 1. `sameAs` Entity Array Declarations

Embed authoritative entity references in your top-level `Organization` and `Brand` Schema.org definitions:

```json
{
  "@context": "https://schema.org",
  "@type": "Brand",
  "name": "Acme Athletics",
  "url": "https://example.com",
  "sameAs": [
    "https://www.wikidata.org/wiki/Q12345678",
    "https://en.wikipedia.org/wiki/Acme_Athletics",
    "https://www.google.com/search?kgmid=/g/11bxxyz"
  ]
}
```

---

## 2. Sitemap `<lastmod>` & Schema `dateModified`

- Every indexed product URL in `sitemap.xml` must include an accurate `<lastmod>YYYY-MM-DDThh:mm:ssTZD</lastmod>`.
- Product JSON-LD should supply `"dateModified": "2026-09-01T12:00:00Z"` to inform LLMs of recent specification or pricing updates.

---

## 3. Brand Truth Standard (`/.well-known/brand-truth.json`)

Publish a deterministic brand truth file to eliminate AI hallucinations regarding policies, warranties, and canonical product specs:

```json
{
  "$schema": "https://agentskills.io/schemas/brand-truth.v1.json",
  "brand_name": "Acme Athletics",
  "official_domain": "example.com",
  "headquarters": "San Francisco, CA",
  "policies": {
    "return_window_days": 30,
    "warranty_duration_months": 24,
    "free_shipping_threshold_usd": 50.00
  },
  "canonical_entity_ids": {
    "wikidata_id": "Q12345678",
    "kgmid": "/g/11bxxyz"
  }
}
```

