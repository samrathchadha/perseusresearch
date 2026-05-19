// Astro's Shiki transformer fires before user rehype plugins and converts
// ```mermaid fences into <pre class="astro-code" data-language="mermaid">
// with tokenized <span> children. By that point rehype-mermaid (which
// looks for class="language-mermaid") no longer matches, so SVG rendering
// silently skips. This plugin runs BEFORE rehype-mermaid in the rehype
// chain and rewrites Shiki-highlighted mermaid blocks back into the
// canonical <pre><code class="language-mermaid">…</code></pre> shape that
// rehype-mermaid expects.

function collectText(node) {
  if (!node) return "";
  if (node.type === "text") return node.value || "";
  if (Array.isArray(node.children)) {
    return node.children.map(collectText).join("");
  }
  return "";
}

function walk(node) {
  if (!node || !Array.isArray(node.children)) return;
  for (let i = 0; i < node.children.length; i++) {
    const child = node.children[i];
    if (
      child.type === "element" &&
      child.tagName === "pre" &&
      child.properties?.dataLanguage === "mermaid"
    ) {
      const raw = collectText(child);
      node.children[i] = {
        type: "element",
        tagName: "pre",
        properties: {},
        children: [
          {
            type: "element",
            tagName: "code",
            properties: { className: ["language-mermaid"] },
            children: [{ type: "text", value: raw }],
          },
        ],
      };
      continue;
    }
    walk(child);
  }
}

export default function rehypeUnshikiMermaid() {
  return (tree) => walk(tree);
}
