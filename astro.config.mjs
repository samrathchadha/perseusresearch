import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import rehypeMermaid from "rehype-mermaid";

// https://astro.build/config
export default defineConfig({
  site: "https://perseus.starling.sh",
  output: "static",
  build: {
    format: "directory",
  },
  integrations: [mdx()],
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [
      [rehypeKatex, { output: "mathml" }],
      [
        rehypeMermaid,
        {
          strategy: "img-svg",
          mermaidConfig: { theme: "neutral" },
        },
      ],
    ],
  },
});
