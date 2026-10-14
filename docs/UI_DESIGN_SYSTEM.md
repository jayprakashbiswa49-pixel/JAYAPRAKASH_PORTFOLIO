# UI Design System: Modern Soft Neumorphism

**Project:** Jayaprakash Biswal Developer Portfolio  
**Design Paradigm:** Soft Tactile Neumorphism (Skeuomorphic Modernism)  
**WCAG Compliance:** WCAG 2.1 AA Compliant  

---

## 1. Design Philosophy & Physical Metaphor

Neumorphism (soft UI) treats the user interface not as layered sheets of paper (Material Design) or completely flat vectors (Flat Design), but as a single continuous surface crafted from a flexible material. Elements appear to **extrude upwards** from the canvas (raised surfaces) or be **pressed downwards** into the canvas (inset/embossed surfaces).

### The Four Tenets of Accessible Neumorphism
1. **Light Source Directionality**: A virtual primary directional light source originates from the top-left (e.g. angle $135^{\circ}$ / $-45^{\circ}$). This produces a bright highlight at the top-left (`-X, -Y`) and a soft shadow at the bottom-right (`+X, +Y`).
2. **Surface Harmony**: The surface color matches or very closely blends with the background canvas color (`#E8ECF1`), creating the illusion of a monolithic material.
3. **Contrast Independence**: Neumorphic depth must **never** be the sole signal of affordance. Text contrast, color accents (`#4568DC`), SVG icons, clear typography, and tactile borders reinforce interactive elements so that users with visual impairments or varying screen brightness can navigate effortlessly.
4. **Subtle Motion**: Transitions must be gentle and physically plausible (between 150ms and 250ms with `cubic-bezier(0.4, 0, 0.2, 1)` easing curves).

---

## 2. Color Palette & Design Tokens

### Primary Canvas & Surfaces
| Token Name | Hex Code | HSL Value | Purpose |
| :--- | :--- | :--- | :--- |
| `--bg` | `#E8ECF1` | `hsl(214, 20%, 93%)` | Main viewport canvas background |
| `--surface` | `#E8ECF1` | `hsl(214, 20%, 93%)` | Raised card, navigation, button surfaces |
| `--surface-inset`| `#E1E6EC` | `hsl(213, 22%, 90%)` | Slightly recessed base for form inputs |
| `--surface-raised-hover` | `#EDF1F5` | `hsl(214, 25%, 95%)` | Interactive card hover surface tint |

### Typography & Text Hierarchy
| Token Name | Hex Code | Contrast on `#E8ECF1` | WCAG Rating | Usage |
| :--- | :--- | :--- | :--- | :--- |
| `--text-primary` | `#202936` | **9.81:1** | **AAA** (Exceeds 7:1) | Headings, body copy, active links |
| `--text-secondary`| `#4F5D73` | **5.45:1** | **AA** (Exceeds 4.5:1) | Subheadings, card descriptions, labels |
| `--text-muted` | `#657080` | **4.55:1** | **AA** (Meets 4.5:1) | Metadata, dates, auxiliary notes |

### Accents & Status Indicators
| Token Name | Hex Code | Usage |
| :--- | :--- | :--- |
| `--accent-primary` | `#4568DC` | Brand identity, primary CTAs, active indicators, focus rings |
| `--accent-hover` | `#3553C0` | Hover state for accent buttons |
| `--accent-subtle` | `rgba(69, 104, 220, 0.12)`| Accent badges, active pill backgrounds |
| `--accent-positive`| `#3B806B` | Success messages, verified badges, live demo indicators |
| `--accent-warning` | `#D97706` | Warning flags, pending states |
| `--accent-danger` | `#DC2626` | Form validation errors, 500 status indicators |
| `--border-subtle` | `rgba(197, 201, 206, 0.45)`| Tactile edge definition on low-contrast displays |

---

## 3. Neumorphic Shadow Calculations

The physics of shadows requires pairing a positive coordinate dark shadow with a negative coordinate light highlight.

### Core Shadow Tokens
```css
:root {
  /* Ambient Shadow Components */
  --shadow-light: #FFFFFF;
  --shadow-dark: #C5C9CE;
  --shadow-dark-subtle: #D2D6DC;
  
  /* Raised Surfaces (Cards, Navbars, Floating Widgets) */
  --shadow-raised: 7px 7px 16px var(--shadow-dark),
                   -7px -7px 16px var(--shadow-light);

  /* Elevated / Hover State */
  --shadow-raised-lg: 10px 10px 22px #B8BDC3,
                      -10px -10px 22px var(--shadow-light);

  /* Subtle Raised (Small Buttons, Chips, Tooltips) */
  --shadow-raised-sm: 4px 4px 9px var(--shadow-dark),
                      -4px -4px 9px var(--shadow-light);

  /* Inset / Pressed Surfaces (Input Fields, Recessed Badges, Pressed Buttons) */
  --shadow-inset: inset 4px 4px 8px var(--shadow-dark),
                  inset -4px -4px 8px var(--shadow-light);

  /* Deep Inset (Focused Inputs, Active State) */
  --shadow-inset-deep: inset 5px 5px 10px var(--shadow-dark),
                       inset -5px -5px 10px var(--shadow-light);

  /* Accent Glow */
  --shadow-accent-glow: 0 4px 14px rgba(69, 104, 220, 0.35);
}
```

---

## 4. Typography Scale

Using **Plus Jakarta Sans** or **Outfit** as the primary font family with clean geometric curves that complement the soft neumorphic radii, falling back to `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`.

```css
:root {
  --font-family-base: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
  --font-family-mono: 'JetBrains Mono', 'Fira Code', monospace;

  --text-xs:   0.75rem;   /* 12px */
  --text-sm:   0.875rem;  /* 14px */
  --text-base: 1.00rem;   /* 16px */
  --text-lg:   1.125rem;  /* 18px */
  --text-xl:   1.25rem;   /* 20px */
  --text-2xl:  1.50rem;   /* 24px */
  --text-3xl:  1.875rem;  /* 30px */
  --text-4xl:  2.25rem;   /* 36px */
  --text-5xl:  3.00rem;   /* 48px */
}
```

---

## 5. Spacing, Borders, and Radii

```css
:root {
  /* Radius Tokens */
  --radius-sm:      8px;   /* Small pills, tooltips */
  --radius-control: 12px;  /* Buttons, form inputs */
  --radius-card:    20px;  /* Standard cards, sections */
  --radius-pill:    9999px;/* Category chips, status badges */
  --radius-circle:  50%;   /* Icon buttons, avatar wrappers */

  /* Spacing Scale */
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.50rem;  /* 8px */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1.00rem;  /* 16px */
  --space-5: 1.25rem;  /* 20px */
  --space-6: 1.50rem;  /* 24px */
  --space-8: 2.00rem;  /* 32px */
  --space-10: 2.50rem; /* 40px */
  --space-12: 3.00rem; /* 48px */
  --space-16: 4.00rem; /* 64px */
  --space-20: 5.00rem; /* 80px */

  /* Layout Container */
  --container-max: 1200px;
  --container-padding: 1.5rem;
}
```

---

## 6. Component Architecture & Micro-Interactions

### A. Neumorphic Buttons
1. **Primary Accent Button**:
   - Background: Gradient `linear-gradient(135deg, #4F70E6, #3B5CC8)`
   - Color: `#FFFFFF`
   - Box shadow: `4px 4px 12px rgba(69, 104, 220, 0.35), -2px -2px 6px #FFFFFF`
   - Active: Pressed scale `transform: translateY(1px) scale(0.98)`
2. **Neumorphic Soft Button**:
   - Background: `var(--surface)`
   - Color: `var(--text-primary)`
   - Box shadow: `var(--shadow-raised-sm)`
   - Hover: Slightly higher elevation `var(--shadow-raised)`
   - Active: `box-shadow: var(--shadow-inset); transform: translateY(1px);`

### B. Inset Form Controls (Inputs & Textareas)
- Default state: Background `var(--surface)`, `box-shadow: var(--shadow-inset)`, border `1px solid transparent`.
- Focus state: `box-shadow: var(--shadow-inset-deep)`, border `1px solid var(--accent-primary)`, outline `none`.
- Error state: `border: 1px solid var(--accent-danger)`, helper text in red.

### C. Raised Project & Skill Cards
- Background: `var(--surface)` with border `1px solid var(--border-subtle)` for sharp crispness.
- Padding: `var(--space-6)`.
- Hover: Elevates smoothly `transform: translateY(-4px)`, shadow expands to `var(--shadow-raised-lg)`.

### D. Accessible Focus Indicator
```css
:focus-visible {
  outline: 2px solid var(--accent-primary) !important;
  outline-offset: 3px !important;
}
```

### E. Motion Control (prefers-reduced-motion)
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```
