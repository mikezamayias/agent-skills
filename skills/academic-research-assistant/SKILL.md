---
name: academic-research-assistant
description: >-
  Synthesize a set of research papers into one literature review of core claims, themes, debates and consensus. Use when asked to analyze, summarize or map several academic papers, articles, PDFs or research documents together.
metadata:
  openclaw:
    emoji: 🎓
    requires:
      tools:
        - pdf
        - read
---

# Academic Research Assistant

Use this skill when the user asks to analyze, summarize, or map a collection of academic papers, articles, or research documents.

Instead of summarizing documents one by one, you will behave like a graduate researcher performing a structured literature review. You will extract core claims, connect the dots, group studies by shared ideas, and identify where authors contradict each other.

## Workflow

When asked to run an academic review on a set of provided documents (PDFs, text files, or URLs):

1. **Ingest the Material**: Use the `pdf` or `read` tools to process the provided documents.
2. **Extract & Map**: Do not summarize them sequentially. Analyze them collectively.
3. **Generate the Synthesis Report**: Output a structured markdown report containing the following exact sections:

### The Synthesis Report Structure

```markdown
# 📚 Literature Review Synthesis

## 1. 🎯 Core Claims

Extract and clearly state the primary thesis or core claim of each study. Keep this extremely concise (1-2 sentences per paper).

## 2. 🧩 Thematic Grouping

Group the studies by shared ideas, methodologies, or theoretical frameworks. Which papers are building on the same foundation? (e.g., "Papers A and B argue for X, while Papers C and D focus on Y").

## 3. ⚡ Active Debates & Contradictions

Highlight exactly where the authors directly contradict each other. What are the conflicting findings or opposing viewpoints across the papers?

## 4. 🤝 The Consensus

Outline the main consensus in the field based on the provided texts. What do all (or most) of the researchers agree on?

## 5. ❓ The Unresolved Question

Identify the single question or gap in the research that remains most unresolved across the entire body of work provided. What needs to be studied next?
```

## Best Practices

- Focus on the synthesis step. The value is in looking _across_ the full set of studies, not summarizing them individually.
- Cite the source documents inline when making claims (e.g., "As demonstrated by Smith (2023)...").
- Maintain a rigorous, objective academic tone.
