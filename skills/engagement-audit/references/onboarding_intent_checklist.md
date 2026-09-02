# On-Site Engagement & Intent Match Checklist

This checklist defines criteria for seamless transitions from LLM conversations to brand website experiences.

---

## 1. Deep-Link Fragment & Anchor Routing

AI chat interfaces often provide users deep-links targeting specific feature sections:
- `https://example.com/shoes/velocity-pro#cushioning`
- `https://example.com/laptop/x1#battery-specs`

### Requirements:
- HTML must contain explicit `id` attributes matching common query targets (`id="specifications"`, `id="cushioning"`).
- Client-side routers (React Router, Next.js) must honor hash fragments after asynchronous component rendering.

---

## 2. Intent Preservation Query Parameter (`?intent=`)

When an AI engine directs traffic with intent context:
`https://example.com/product/123?intent=marathon_training_durability`

### Requirements:
- Ensure server and edge CDN redirects don't discard query parameters.
- Preserve intent tokens in session state to dynamically surface relevant testimonials or technical spec highlights.

---

## 3. Structured `PropertyValue` Schema Specification

Replace vague marketing claims with deterministic PropertyValue schema declarations:

```json
{
  "@type": "PropertyValue",
  "name": "Heel-to-Toe Drop",
  "value": "8",
  "unitCode": "MMT",
  "unitText": "millimeter"
}
```

---

## 4. AI Intent Bridge Micro-Banner

Implement a lightweight, non-intrusive notification badge when `?intent=` or `?ref=ai` is present:
- *"Showing specifications for: Cushioning & Long-Distance Stability"*
- Direct CTA to the corresponding spec table or comparison widget.

