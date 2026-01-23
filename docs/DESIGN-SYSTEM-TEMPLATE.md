# ALPHA MEDICAL - DESIGN SYSTEM TEMPLATE
## Version: 1.0.0 | Created: 23/01/2026 | Session 144
## Transferred from 3A via Technology Shelf (Étagère Technologique)

> **Ce document est un template de Design System adapté pour Shopify.**
> Basé sur le Design System 3A Automation.

---

## 1. BRAND COLORS (Adapt to Alpha Medical)

```css
:root {
  /* Primary - Adapt to your brand */
  --primary: #YOUR_BRAND_COLOR;
  --primary-dark: #DARKER_VARIANT;
  --primary-light: #LIGHTER_VARIANT;

  /* Semantic Colors (Keep standard) */
  --success: #10B981;
  --warning: #F59E0B;
  --error: #EF4444;
  --info: #3B82F6;

  /* Text Colors */
  --text-primary: #1f2937;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;

  /* Backgrounds */
  --bg-primary: #ffffff;
  --bg-secondary: #f9fafb;
  --bg-dark: #111827;
}
```

---

## 2. TYPOGRAPHY

| Element | Size | Weight | Line Height |
|---------|------|--------|-------------|
| H1 | 2.5rem | 700 | 1.2 |
| H2 | 2rem | 600 | 1.3 |
| H3 | 1.5rem | 600 | 1.4 |
| Body | 1rem | 400 | 1.6 |
| Small | 0.875rem | 400 | 1.5 |

**Font Stack:** `'Inter', system-ui, -apple-system, sans-serif`

---

## 3. SPACING SCALE

| Token | Value | Usage |
|-------|-------|-------|
| `--space-1` | 0.25rem | Tight spacing |
| `--space-2` | 0.5rem | Small gaps |
| `--space-3` | 0.75rem | Default gap |
| `--space-4` | 1rem | Standard spacing |
| `--space-6` | 1.5rem | Section padding |
| `--space-8` | 2rem | Large spacing |

---

## 4. COMPONENT PATTERNS

### Buttons
```css
.btn-primary {
  background: var(--primary);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
}

.btn-primary:hover {
  background: var(--primary-dark);
}
```

### Cards
```css
.card {
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
```

---

## 5. SHOPIFY LIQUID INTEGRATION

### Theme Settings Reference
```liquid
{% assign primary_color = settings.primary_color | default: '#4FBAF1' %}
{% assign secondary_color = settings.secondary_color | default: '#191E35' %}
```

### Section Schema Pattern
```json
{
  "settings": [
    {
      "type": "color",
      "id": "background_color",
      "label": "Background Color",
      "default": "#ffffff"
    }
  ]
}
```

---

## 6. VALIDATION CHECKLIST

- [ ] All colors use CSS variables
- [ ] No hardcoded hex values in sections
- [ ] Consistent spacing using tokens
- [ ] Accessible color contrast (4.5:1 min)
- [ ] Mobile-first responsive styles

---

## 7. TECHNOLOGY SHELF REFERENCE

| Origin | Pattern | Adaptation |
|--------|---------|------------|
| 3A | CSS Variables | Shopify theme settings |
| 3A | Glassmorphism | Card hover effects |
| 3A | Spacing scale | Section padding |
| 3A | Typography | Heading hierarchy |

---

*Transferred via Étagère Technologique - Session 144*
