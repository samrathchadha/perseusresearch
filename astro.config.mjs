import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import rehypeMermaid from "rehype-mermaid";

const remarkPlugins = [remarkMath];
const rehypePlugins = [
  [rehypeKatex, { output: "mathml" }],
  [
    rehypeMermaid,
    {
      // inline-svg: rehype-mermaid spawns Playwright/Chromium at build,
      // renders each mermaid block to SVG, inlines the SVG in the HTML.
      // No client-side JS for diagrams. Search-indexable, FOUC-free.
      // Requires `playwright install chromium` in the build script.
      strategy: "inline-svg",
      mermaidConfig: {
        theme: "neutral",
        themeVariables: {
          fontFamily: "'Adobe Garamond Pro', 'EB Garamond', Times, serif",
          fontSize: "14px",
          primaryColor: "#fafaf7",
          primaryTextColor: "#1a1815",
          primaryBorderColor: "#6b6157",
          lineColor: "#6b6157",
          secondaryColor: "#f6f4ee",
          tertiaryColor: "#ffffff",
          background: "#ffffff",
        },
        flowchart: { curve: "basis", padding: 12 },
      },
    },
  ],
];

const shikiConfig = {
  theme: "github-light",
  wrap: true,
};

// https://astro.build/config
export default defineConfig({
  site: "https://perseus.starling.sh",
  output: "static",
  build: {
    format: "directory",
  },
  integrations: [
    mdx({
      remarkPlugins,
      rehypePlugins,
      shikiConfig,
    }),
  ],
  markdown: {
    remarkPlugins,
    rehypePlugins,
    shikiConfig,
  },
});
