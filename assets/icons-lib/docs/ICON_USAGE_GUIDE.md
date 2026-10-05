# Chit UI Asset Package

## Contents

- `master-icon-board.png`: design-review board generated for the Chit visual direction.
- `icons/`: **transparent, color-agnostic SVG source icons**, one icon per file.
- `chit-icons.svg`: combined SVG symbol sprite.
- `chit-icons.ts`: typed TypeScript registry and search helper.
- `icon-registry.json`: neutral machine-readable registry.
- `figma/README.md`: import and component-library guidance.
- `previews/`: light and dark theme reference sheets.

## Implementation contract

Each source SVG has a transparent background and uses `currentColor`. The consuming component—not the icon file—must control size, color, contrast, surface, focus state, hover state, and shadow.

```tsx
import SolarIcon from './assets/icons/energy/solar.svg?react';

export function EnergyMetric() {
  return <SolarIcon className="chit-icon chit-icon--energy" aria-label="Solar generation" />;
}
```

```css
.chit-icon {
  inline-size: 24px;
  block-size: 24px;
  color: var(--icon-default);
  flex: none;
}
.chit-icon--energy { color: var(--domain-energy); }
```

## SVG sprite

```html
<svg class="chit-icon" aria-hidden="true">
  <use href="/assets/chit-icons.svg#solar"></use>
</svg>
```

The sprite uses a 24 × 24 viewBox, rounded line caps/joins, `fill="none"`, `stroke="currentColor"`, and a 1.8 stroke width.

## Tokens

```css
:root {
  --icon-default: #21314b;
  --icon-muted: #65738a;
  --icon-active: #267cf0;
  --domain-energy: #b87800;
  --domain-climate: #087bb5;
  --domain-security: #067852;
  --domain-family: #7045c4;
  --domain-health: #c22b76;
  --state-success: #087b54;
  --state-warning: #a85d00;
  --state-critical: #bd2447;
}

[data-theme="dark"] {
  --icon-default: #d7e5f7;
  --icon-muted: #91a3bd;
  --icon-active: #65b4ff;
  --domain-energy: #f7c847;
  --domain-climate: #58c7ff;
  --domain-security: #47e0ac;
  --domain-family: #ba92ff;
  --domain-health: #ff8bc2;
  --state-success: #48e0a9;
  --state-warning: #ffc35a;
  --state-critical: #ff7890;
}
```

## Accessibility

- Decorative icon: use `aria-hidden="true"`.
- Icon-only interactive control: provide an explicit `aria-label`, such as `aria-label="Open family calendar"`.
- Do not convey health, security, location, or task urgency through color alone. Include text, a status label, or an accessible description.
- Keep touch targets at least 44 × 44 CSS pixels for the wall-panel / family interface.
- Use a clear focus ring that meets contrast requirements on both themes.

## State rules

- **Neutral**: ordinary available control or unremarkable metric.
- **Active**: selected navigation or currently enabled setting.
- **Domain tone**: identifies the conceptual area; for example amber for energy or pink for health.
- **Success / warning / critical**: identifies a condition, never merely an aesthetic variation.
- **Muted / offline**: unavailable, inactive, stale, or deliberately withheld data.

## Do / don't

### Do
- Use transparent SVG files and theme tokens.
- Keep icons at whole-pixel sizes where possible: 16, 20, 24, 32, 40, 48.
- Pair sensitive information with text: `Location hidden`, `Health data private`, `Attention required`.
- Use labelled variants for family location, health metrics, and security states.

### Don't
- Do not add card backgrounds, gradients, or glow directly into an icon source file.
- Do not encode a state using color alone.
- Do not force a 16px icon into a 48px hero area; use the correct size token.
- Do not expose exact location or detailed health data in the wall-display view by default.

## Notes

The master board is a visual reference. The hand-authored SVGs in this package are the implementation assets. They are deliberately transparent and use `currentColor` so that the same source works in light, dark, high-contrast, domain-colored, and status-colored contexts.
