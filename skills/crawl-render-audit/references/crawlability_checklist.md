# Crawlability & Rendering Verification Checklist

This checklist provides standard verification items and remediation steps for AI crawlers and rendering architectures.

---

## 1. `robots.txt` AI Crawler Matrix

Ensure relevant AI crawlers are granted access to public catalog pages:

| User-Agent | AI Engine / Service | Recommended Status |
| :--- | :--- | :--- |
| `GPTBot` | OpenAI ChatGPT Web Search / SearchGPT | **Allow** on public catalog |
| `PerplexityBot` | Perplexity AI Search | **Allow** on public catalog |
| `ClaudeBot` / `anthropic-ai` | Anthropic Claude Search / Coworkers | **Allow** on public catalog |
| `Google-Extended` | Google Gemini / Bard AI Overviews | **Allow** on public catalog |
| `Amazonbot` | Amazon Rufus / AI Assistant | **Allow** on public catalog |
| `CCBot` | Common Crawl (Base training data) | Disallow only if copyright opt-out required |

---

## 2. CSR vs SSR Density Audit

- **Threshold:** If raw static HTML word count is $< 30\%$ of rendered DOM word count, flag as `critical` severity.
- **Remediation:** Implement Server-Side Rendering (SSR), Static Site Generation (SSG), or Edge HTML pre-rendering dynamically triggered for AI crawler User-Agents.

---

## 3. Schema.org JSON-LD Verification

Validate that every product and organization page contains:

```json
{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "Sample Product",
  "image": ["https://example.com/photos/1x1/photo.jpg"],
  "description": "Comprehensive spec description",
  "sku": "0446310786",
  "brand": {
    "@type": "Brand",
    "name": "BrandName"
  },
  "offers": {
    "@type": "AggregateOffer",
    "priceCurrency": "USD",
    "lowPrice": "119.99",
    "highPrice": "149.99",
    "offerCount": "8"
  }
}
```

---

## 4. `/llms.txt` Standard

Provide a concise, curated markdown overview of the website at `/llms.txt`:
- Project / Brand mission
- Key product lines & canonical URLs
- Direct link to full markdown catalog `/llms-full.txt`

