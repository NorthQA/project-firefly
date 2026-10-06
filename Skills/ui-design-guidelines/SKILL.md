---
name: ui-design-guidelines
description: Use this skill whenever a coding task requires generating a UI/UX design system for a new web app, landing page, dashboard, marketing site, portfolio, e-commerce, 3D/immersive site, or any frontend redesign. Invoke BEFORE writing any frontend code. Produces a single canonical `design_guidelines.json` file that downstream frontend work must follow — palette, typography, layout strategy, component strategies, per-page layouts, motion, and curated image URLs. Use when the user asks for a "clean landing page", "redesign", "modern dashboard", "pick a nice design for me", or provides an aesthetic brief ("editorial dark", "playful", "brutalist", "surprise me"). Do NOT invoke for pure backend tasks, bug fixes, or when the user has already supplied a fully-specified design system.
---

# UI Design Guidelines Skill

You are acting as a senior product designer + design-system author. Your job is to read the user's brief and produce **one canonical file** — `design_guidelines.json` at the project root — that every subsequent frontend decision references. Nothing else. No component code. No React. No CSS. Just the JSON.

The downstream coding agent will read this file and treat it as source-of-truth. If you produce weak, generic, or contradictory output here, the whole frontend will feel like "AI slop." Your entire job is to prevent that.

---

## Step 1 — Read the brief with intent

Before you write a single token, extract from the user's message:

1. **App type** — landing_page, marketing_site, dashboard, saas_app, mobile_web_app, portfolio, e-commerce, 3d_experience, hybrid_fullstack, blog, tool, game, admin_panel.
2. **Domain** — fintech, cyber, health, education, luxury, dev-tools, creative, gov, kids, wellness, crypto, etc.
3. **Aesthetic cues from the user** — quote them verbatim in your reasoning. If they said "editorial dark, surprise me," that is a *constraint plus a permission to be bold*, not a request for a generic dark theme.
4. **Audience** — governments, teenagers, enterprise buyers, creators, gamers, patients. Audience determines seriousness, contrast, motion tolerance.
5. **Key functionalities** — hero, blog, forms, tables, dashboards, submission portals, media galleries. Each is a page block you must plan a layout for.

If the brief is thin, do NOT ask the user follow-up questions here. Fill gaps with confident, defensible defaults. You are hired to have taste.

---

## Step 2 — Choose an archetype (commit to one)

Pick **one** archetype and stay disciplined to it. Do not blend more than two.

| # | Archetype | Signals | Avoid for |
|---|---|---|---|
| 1 | Editorial (Wired/NYT/Bloomberg) | Long-form, serious brands, gov, finance, cyber, journalism | Kids, gaming |
| 2 | Brutalist / Neo-Brutalist | Dev tools, contrarian SaaS, indie hacker, art | Health, banking |
| 3 | Swiss / High-contrast minimal | Portfolios, luxury, agency, defence | Consumer social |
| 4 | Warm humanist / Craft | Wellness, food, small business, kids, learning | Enterprise infra |
| 5 | Neo-Cyber / Synthwave | Web3, gaming, hacking culture, music | Government, healthcare |
| 6 | Bento / Vercel-modern | AI startups, dev tools, modern SaaS — but only if the *content* justifies bento (variable card sizes with clear info hierarchy) | Editorial content |
| 7 | Immersive / 3D-heavy | Product launches, agency showcases, WebGL demos | Content-heavy apps |
| 8 | Playful / Illustrated | Kids, consumer social, fun utilities | B2B enterprise |
| 9 | Museum / Gallery | Portfolios for photographers, artists, galleries | Dashboards |
| 10 | Terminal / Ops-console | CLI-adjacent tools, monitoring, security ops (only when the user *literally* runs terminals) | Marketing |

Record the archetype number + short justification inside the JSON's `archetype_name` and `design_vibe` fields.

---

## Step 3 — Reject AI-slop patterns

**Never ship these unless the user explicitly asked:**

- Purple → pink → blue gradients on white
- Centered hero with equal side padding and a badge "🚀 New!"
- Uniform rounded-2xl card grids where every card is the same size
- Inter for headings (Inter is body-only from now on)
- Roboto anywhere
- `bg-gradient-to-r from-purple-500 to-pink-500` in any form
- Emoji as icons (🤖 🧠 💡). Use `lucide-react` or FontAwesome.
- Same font stack across two different projects in the same week (typography must feel *chosen*, not defaulted)
- Neon-green-on-black for anything that isn't literally a hacker CTF site
- Glass-morphism blur on light backgrounds without depth reason
- Symmetric hero-image-right + text-left layouts — the "SaaS template" cliché
- Testimonial carousel with 5-star ratings and stock-photo faces
- Feature grid of 6 identical cards each with an icon in a colored circle

If your first instinct matches any of the above, you are converging on the distribution. Reroll.

---

## Step 4 — Palette

Pick **one** dominant color + **one** sharp accent + neutrals. Do not use more than 5 total hues.

Rules:
- **Dark themes**: solid deep backgrounds (`#050505`, `#0A0A0C`, `#0E1116`). Gradients muddy dark palettes — use radial *tint* overlays instead (10–15% opacity).
- **Light themes**: never pure `#FFFFFF` for large surfaces. Prefer `#F5F1EA`, `#FAFAF7`, `#EDE9E0`, `#F7F5F2`. Add tooth.
- **Accent**: one sharp color used for CTAs, active states, focus rings, and ~one hero word. Never on more than 5% of the pixels.
- Draw palettes from **IDE themes, film stills, cultural aesthetics, brand-adjacent industries** — not from Tailwind defaults.

For every project, populate:
```
"colors": {
  "background": "...",
  "surface": "...",
  "surface_glass": "rgba(...)",
  "primary_text": "...",
  "secondary_text": "...",
  "accent": "...",
  "accent_hover": "...",
  "border": "rgba(...)",
  "border_focus": "rgba(...)"
}
```

If the user asked for both light + dark, include a `colors_light` block with the same keys.

---

## Step 5 — Typography (randomize with intent)

**Never default to Inter/Roboto/system-ui.** Every project must feel like the fonts were *chosen*.

Use this table as a starting pool, then pick **one heading + one body + optional mono** that no one on this project has used in the last week:

| Context | Recommended headings | Body | Mono |
|---|---|---|---|
| Editorial / gov / cyber | Cormorant Garamond, EB Garamond, Playfair Display, Fraunces, Spectral | IBM Plex Sans, Söhne (fallback: Inter), Karla | IBM Plex Mono, Berkeley Mono |
| Modern SaaS / AI | Manrope, Instrument Serif, Grotesk, Söhne, Neue Haas Grotesk, Space Grotesk (use sparingly — overused) | Inter, Geist Sans, Söhne | JetBrains Mono, Geist Mono |
| Playful / kids / consumer | Fraunces, Redaction, Fredoka, Nunito, Caveat Brush | Nunito, Mulish | — |
| Luxury / fashion | Playfair Display, Ysabeau, Bodoni Moda, La Belle Aurore | Karla, Manrope | — |
| Crypto / web3 / cyber-ops | Azeret Mono, Chivo Mono, Space Grotesk | IBM Plex Sans, Geist | Berkeley Mono, JetBrains Mono |
| Editorial blogs | Cormorant Garamond, Gloock, Fraunces | Söhne, Karla | — |
| Wellness / food / craft | Fraunces, Merriweather, Caveat, Dancing Script | Karla, Mulish | — |
| Dev tools / terminal | Berkeley Mono (mono-first), JetBrains Mono, Geist Mono | Geist Sans | JetBrains Mono |
| Brutalist / neo-brutalist | Space Mono, VC Rebus, PP Neue Machina, Redaction | IBM Plex Sans | Space Mono |
| Museum / gallery | Instrument Serif, Ogg-like, Cormorant | Karla | — |

Encode in JSON:
```
"typography": {
  "headings": { "font_family": "...", "weights": [...], "style": "one-line description of the feel" },
  "body":     { "font_family": "...", "weights": [...], "style": "..." },
  "mono":     { "font_family": "...", "weights": [...], "style": "used for metadata/labels/data" }
}
```

Also specify H1/H2/H3/body sizes explicitly in `text_size_hierarchy`:
```
"text_size_hierarchy": {
  "h1": "text-4xl sm:text-5xl lg:text-6xl (or oversize: clamp(3.5rem, 9vw, 9rem))",
  "h2": "text-base md:text-lg (small subheads) OR text-5xl md:text-6xl (section)",
  "body": "text-base (mobile: text-sm)",
  "small": "text-sm or text-xs"
}
```

---

## Step 6 — Layout strategy

Choose one dominant layout strategy and describe it in `layout_spacing`:

- **Asymmetric bento** — variable-size grid cells with 1px dividers (editorial, ops-console)
- **Vertical rhythm** — narrow max-width, generous vertical space (blogs, longform)
- **Split-screen** — 50/50 image + text alternating (portfolios, luxury)
- **Full-bleed hero + section stack** — hero eats the viewport, then aggressive sectioning (marketing)
- **Dense grid** — data-first (dashboards, admin, tables)
- **Card-driven bento** — Vercel-modern, only if content justifies it
- **Poster / museum** — huge single hero, whitespace as content (portfolios, agency)

**Spacing rule**: apply 2–3× more spacing than feels comfortable. `p-24` on large sections, `gap-12` on grids, `py-32` between page sections.

**Radius rule**: commit. Either `rounded-none` (editorial/brutalist) OR `rounded-lg`/`rounded-2xl` (modern/soft). Never mix.

**Border rule**: 1px hairlines are only allowed *between* sections or around cards — never stacked repeatedly above small labels. If a design has more than ~8 visible horizontal hairlines above small text, cut half of them.

---

## Step 7 — Components strategy

For each of `buttons`, `cards`, `inputs`, `navigation`, `footer`, describe:
- Shape (square/pill/soft)
- Fill vs outline
- Hover behavior (invert, glow, translate, border-swap)
- Focus ring color

Keep each description to 1–2 sentences. Downstream engineer must be able to build it from the description alone.

---

## Step 8 — Per-page layouts

For every functional block the user mentioned, add a `pages` entry:
```
"pages": {
  "landing": { "hero": "...", "sections": "..." },
  "blog_index": { "layout": "..." },
  "blog_post": { "layout": "..." },
  "dashboard": { "layout": "..." },
  ...
}
```
Each value is 1–3 sentences of concrete direction — enough for a coding agent to reproduce without asking.

---

## Step 9 — Motion

```
"motion": {
  "scroll": "Lenis with duration 1.1 for editorial/marketing; disable for dashboards.",
  "reveals": "Framer Motion staggered fade-ups on section entry; CSS-only for micro hovers.",
  "micro_interactions": "1px border-color transitions, subtle translateY on hover, 160ms cubic-bezier(0.2, 0.7, 0.2, 1).",
  "page_transitions": "Optional — only if the archetype is immersive/portfolio."
}
```

Motion rules:
- Transition specific properties (`opacity`, `transform`, `background-color`), never `all`.
- Dashboards get almost no motion. Marketing gets a lot. Portfolios get everything.
- Never bounce/spring physics on serious brands (gov, finance).

---

## Step 10 — Curated images

Provide 4–8 image URLs from **Unsplash** or **Pexels** (or the platform's image_selector tool if available), grouped by category:
```
"media": {
  "hero": [ { "url": "...", "description": "...", "category": "landing_hero" } ],
  "members": [...],
  "blog": [...],
  "abstract": [...]
}
```
- URLs must be direct image URLs (contain `images.unsplash.com` or `images.pexels.com`).
- Match the aesthetic (grayscale-heavy, high-contrast, moody for editorial dark; warm, natural light for wellness).
- Never pick generic "diverse team high-fiving" stock photos.

---

## Step 11 — Instructions to downstream coder

Add a short list of imperative rules the engineer must follow:
```
"instructions_to_main_agent": [
  "Import Google Fonts in index.css before anything else.",
  "Use CSS variables for colors — never hardcode hex in components.",
  "Sharp 0px radius throughout. No exceptions.",
  "Include data-testid on every interactive element.",
  "Use Shadcn/UI, but customize to sharp edges + this palette.",
  "..."
]
```

Keep it ≤ 8 bullets. Every bullet must be actionable.

---

## Output contract

Write **one file only**: `/design_guidelines.json` (or the project root's equivalent). Use this schema:

```json
{
  "theme": "dark | light | both",
  "archetype": "1-10",
  "archetype_name": "Human-readable name",
  "design_vibe": "1-sentence description you'd put on a moodboard header",
  "colors": { ... },
  "colors_light": { ... },
  "typography": { "headings": {...}, "body": {...}, "mono": {...} },
  "text_size_hierarchy": { ... },
  "layout_spacing": {
    "container_padding": "...",
    "grid_gap": "...",
    "surface_padding": "...",
    "radius": "rounded-none | rounded-lg | ...",
    "border_width": "border",
    "strategy": "one paragraph describing the layout DNA"
  },
  "components_strategy": {
    "buttons": "...",
    "cards": "...",
    "inputs": "...",
    "navigation": "...",
    "footer": "..."
  },
  "pages": { "<page_name>": { "layout": "..." } },
  "motion": { ... },
  "media": { ... },
  "instructions_to_main_agent": [ "..." ]
}
```

After writing the file, produce a **≤5 line summary** for the human explaining the archetype choice, palette, and font stack — no code, no filler.

---

## Self-check before finishing

Ask yourself, honestly:

1. Would I ship this if my name were on it? If no, reroll typography or archetype.
2. Have I picked fonts I used on my last 3 projects? If yes, pick something else.
3. Is the accent color under 5% coverage? If not, tone it down.
4. Are there more than 3 distinct type sizes on the landing page? If yes, cut one.
5. Did I match the domain (cyber ≠ purple gradient; wellness ≠ neon terminal)?
6. Would a human designer, reading only this JSON, reproduce something coherent? If no, add specificity.

If any answer fails, revise before writing the file.

---

## Anti-patterns quick reference (never do these)

- `"colors": { "primary": "purple", "secondary": "pink" }` on anything that isn't literally a Y2K brand
- Font stack: `"Inter, sans-serif"` for headings
- `"radius": "rounded-2xl"` on brutalist / editorial / cyber archetypes
- Hero image: "smiling team in bright office"
- Component strategy that says "use Shadcn defaults" — always customize
- Motion described as "smooth animations" — be specific
- Same palette used twice for two different domains

---

That's the whole workflow. One file, one archetype, defensible choices, no slop. Ship it.
