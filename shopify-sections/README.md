# Zack AI — Modular Shopify Sections

This folder contains modular, reusable Liquid sections and snippets designed to showcase Zack AI on product pages while optimizing for conversion.

## Files

- `sections/product-tech-specs.liquid` — Detailed technical specifications grid
- `sections/product-use-cases.liquid` — Card‑based use cases
- `sections/product-software-compatibility.liquid` — Software features and compatibility notes
- `sections/product-trust.liquid` — Certifications, privacy bullets, testimonials
- `sections/product-urgency-preorder.liquid` — Countdown + limited availability + pre‑order CTA
- `snippets/zack-countdown.liquid` — Lightweight countdown (no external libs)
- `snippets/zack-cta.liquid` — Streamlined pre‑order button (form → add to cart)
- `snippets/zack-cert-badges.liquid` — Simple certification badges (text)
- `assets/zack-modules.css` — Minimal responsive styling shared by sections

## Install in a Shopify Theme (Online Store 2.0)

1. Copy files into your theme:
   - `sections/*` → `theme/sections/`
   - `snippets/*` → `theme/snippets/`
   - `assets/zack-modules.css` → `theme/assets/`
2. Open `theme-customizer` and add sections to the Product template in the order:
   - Urgency & Pre‑Order CTA → Use Cases → Software → Technical Specs → Trust
3. Configure settings:
   - Set `product_handle` in Urgency section if using on non‑product pages.
   - Set `countdown_end` (ISO date, e.g., `2025-11-30T23:59:59Z`).
   - Optionally enable `inventory` display or set `limited_qty` fallback.
   - Edit copy directly in section blocks. Defaults are pre‑filled from guardrails.
4. Branding:
   - Sections rely on `assets/zack-modules.css` for minimal layout; they inherit your theme’s fonts/colors. Adjust CSS variables if needed (`--z-primary`, `--z-text`, etc.).
5. Performance:
   - No heavy JS; only a tiny countdown script (deferred by placement).
   - Images and icons are not bundled; reuse theme assets or add as needed.

## Notes & Safety

- The content defaults align with `/00-foundation/zack-ai-product-guardrails.md` and avoid unsupported claims.
- Voice cloning is opt‑in and requires verified parental consent — keep disclaimer visible.
- Privacy bullets mirror GDPR/COPPA/CCPA alignment and local processing defaults.

## Optional Enhancements

- Replace text badges with SVG logos in a new snippet or with image blocks.
- Add dynamic source bindings for `product` in sections if using outside product pages.
- Hook secondary CTA to `#z-tech-specs` or a dedicated page for full specs.

## QA Checklist

- Verify `zack-modules.css` loads (no 404s) in theme.
- Confirm countdown date/timezone displays correctly on mobile and desktop.
- Test pre‑order button with the selected variant; ensure cart add works.
- Validate inventory message (or fall back to limited quantity).
- Review mobile spacing and tap targets for CTAs.
