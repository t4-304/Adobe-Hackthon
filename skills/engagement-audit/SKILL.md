---
name: engagement-audit
description: >-
  Audits on-site engagement, deep-link preservation, and intent alignment. Detects broken
  deep-link hash fragments, query intent parameter stripping, absent PropertyValue schemas,
  and missing AI Intent Bridge micro-banners.
---

# On-Site Engagement & Intent Match Skill

Evaluates how well a brand's web pages preserve arriving AI context and satisfy user intent. Addresses **Round 2 Failure Modes 3 & 4: Landing Friction & Spec Hallucination**.

## Core Verification Areas

1. **Deep-Link Fragment & Query Parameter Preservation:**
   - Verifies whether URL hash fragments (`#specifications`, `#cushioning`, `#sizing`, `#battery-life`) auto-scroll and highlight target elements.
   - Evaluates whether query parameters (`?intent=cushioning_comparison&ref=ai`) are preserved through client-side routing rather than stripped by redirects.

2. **Technical Biomechanical & PropertyValue Spec Tables:**
   - Audits product specification tables for structured `additionalProperty` / `PropertyValue` markup vs. ambiguous marketing copy.
   - Ensures quantitative specs (weight in grams, heel-to-toe drop in mm, battery capacity in mAh) are unambiguous.

3. **AI Intent Bridge Micro-Banners:**
   - Detects dynamic UI micro-banners that acknowledge the user's arriving query context and display targeted comparison badges.

## Usage

```bash
python scripts/check_engagement.py --url https://example.com
```

## References

- [Onboarding Intent Checklist](./references/onboarding_intent_checklist.md)

