import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import rehypeMermaid from "rehype-mermaid";
import rehypeUnshikiMermaid from "./src/lib/rehype-unshiki-mermaid.mjs";

// Vercel's build image is Amazon Linux and Playwright's downloaded
// Chromium (Ubuntu-built) is missing system libs like libnspr4.so.
// On Linux we use @sparticuz/chromium, a serverless-bundled binary
// that ships its own deps. On macOS we use Playwright's default.
const launchOptions =
  process.platform === "linux"
    ? await (async () => {
        const { default: chromium } = await import("@sparticuz/chromium");
        return {
          args: chromium.args,
          executablePath: await chromium.executablePath(),
          headless: true,
        };
      })()
    : { headless: true };

const shikiConfig = {
  theme: "github-light",
  wrap: true,
};

const remarkPlugins = [remarkMath];
// rehypeUnshikiMermaid MUST come before rehypeMermaid: Astro's Shiki
// transformer turns ```mermaid fences into <pre class="astro-code"
// data-language="mermaid"> by the time user rehype plugins run. The
// unshiki step rewrites those back to the <pre><code class="language-mermaid">
// shape that rehype-mermaid scans for.
const rehypePlugins = [
  [rehypeKatex, { output: "mathml" }],
  rehypeUnshikiMermaid,
  [
    rehypeMermaid,
    {
      // inline-svg: rehype-mermaid renders each mermaid block to inline SVG
      // at build time via Playwright/Chromium. No client-side mermaid JS;
      // diagrams ship in the HTML, search-indexable, FOUC-free.
      strategy: "inline-svg",
      launchOptions,
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
