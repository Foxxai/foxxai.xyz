# Content Staging Area

This directory contains drafts and supporting materials for content generation:

```text
docs/_entries_drafts/
├── abstracts/     # LinkedIn-ready summaries
├── essays/        # Longform drafts for foxxai.xyz
├── metadata/      # JSON/YAML front-matter + provenance
└── logs/          # Concept mining logs
```

## Workflow Conventions

1. ChatGPT connector writes to these directories on the `dev` branch only
2. All content remains in draft until manually promoted to live
3. Directory purposes:
   - `abstracts/`: Condensed, professional summaries optimized for LinkedIn
   - `essays/`: Full-length article drafts for the main site
   - `metadata/`: Structured data about content origins and references
   - `logs/`: Records of concept exploration and development

## File Naming

- Standard format: YYYY-MM-DD_slug_v0#.md
  - Date: YYYY-MM-DD
  - Slug: lowercase-with-hyphens
  - Version: v01, v02, etc.
- Examples:
  - 2025-09-14_my-research-topic_v01.md
  - 2025-09-14_my-research-topic_v02.md
- Keep metadata files matched: YYYY-MM-DD_slug_v0#.yaml