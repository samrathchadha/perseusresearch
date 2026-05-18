# perseus essays

Static Astro site for the perseus essays collection.

## Develop

```
npm install
npm run dev
```

Local dev server is served on `http://localhost:4321/` by default.

## Build

```
npm run build
```

Output is a fully static site under `dist/`. Drop it onto any static host:

- Cloudflare Pages: point build command at `npm run build` and output dir at `dist`.
- Netlify: same — `npm run build` / publish dir `dist`.
- GitHub Pages: publish the contents of `dist/` to the `gh-pages` branch.

## Authoring

- Essays live as `.md` / `.mdx` under `src/content/essays/`.
- Front matter is validated by Zod (`src/content/config.ts`). Required fields:
  `title`, `date`, `tier`, `summary`. Optional: `status` (`draft` hides from
  index + routes), `related`, `figures`.
- Math: `$inline$` and `$$display$$` via remark-math + rehype-katex (MathML output).
- Mermaid diagrams: fenced ```mermaid blocks are rendered to SVG at build time
  via rehype-mermaid (`strategy: "img-svg"`).
- Figures: put images under `public/figures/` and reference with the
  `<Figure />` component or plain Markdown.
- Notes / retractions: use the `<Note type="retraction">` component.

## Fonts

Hakumo is loaded locally from `public/fonts/FsHakumoRegular-V49Ky.woff2` (with
TTF fallback) via `@font-face` in `src/styles/global.css`. Body text is Times
New Roman.

## Tiers

The seven canonical tiers (mirrors `Claude.md` and the essay backbone):

1. `pipeline` — Core MuZero pipeline
2. `wm` — World model training
3. `planner` — Planner and Tinker
4. `reward` — Reward and judging
5. `retrieval` — Retrieval as ML
6. `audits` — Audits and meta
7. `infra` — Infrastructure

Order on the landing page is fixed in `src/pages/index.astro`.
