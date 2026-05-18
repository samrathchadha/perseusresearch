import { defineCollection, z } from "astro:content";

const essays = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    status: z.enum(["draft", "published"]).default("published"),
    tier: z.enum([
      "pipeline",
      "wm",
      "planner",
      "reward",
      "retrieval",
      "audits",
      "infra",
    ]),
    summary: z.string(),
    readTime: z.number().optional(),
    related: z.array(z.string()).default([]),
    figures: z
      .array(
        z.object({
          src: z.string(),
          caption: z.string(),
        }),
      )
      .default([]),
  }),
});

export const collections = {
  essays,
};
