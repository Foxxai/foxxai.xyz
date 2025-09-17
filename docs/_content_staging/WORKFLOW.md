# ScholarFlow Content Staging Workflow

This document describes the protocol for drafting, staging, and publishing content in the ScholarFlow system.

## Directory Structure
- `essays/`: Full draft essays (Markdown with YAML header)
- `abstracts/`: Abstracts (Markdown with YAML header)
- `logs/`: Registry and workflow logs
- `README.md`: Staging area documentation

## Process
1. Draft essays and abstracts in their respective folders.
2. Add a minimal YAML header to each file.
3. Append a new row to `logs/registry.csv` with slug, date, type, version, and file path.
4. Commit all staged files with an appropriate message.
5. Move finalized content to the published section (e.g., `/docs/blog/`) for automation and indexing.

Refer to the main project `README.md` for global setup and workflow details.
