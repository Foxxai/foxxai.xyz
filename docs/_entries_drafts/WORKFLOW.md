# ScholarFlow Draft Workflow

## Repository and Branch
- Repo: foxxai.xyz
- Branch: main
- Path: docs/_entries_drafts/

## File Types
- **Essays**: 1,200–1,500 words, structured with H2 sections, and a minimal YAML header:

- **Abstracts**: 120–160 words with the same minimal YAML header.
- **Logs**: `registry.csv` to track every draft (with columns: slug,date,type,version,path).

## Directory Structure
- `essays/` – full drafts (Markdown files with YAML header)
- `abstracts/` – abstracts (Markdown files with YAML header)
- `logs/` – contains `registry.csv`
- `WORKFLOW.md` – this protocol document

## Commit Conventions
- `draft(essay): add <slug> vNN`
- `draft(abstract): add <slug> vNN`
- `docs: update WORKFLOW.md`
- `docs: update registry`

## Process
1. Draft the essay and abstract.
2. Add the minimal YAML header to each file.
3. Append a new row to `logs/registry.csv` with the slug, date, type (essay or abstract), version, and file path.
4. Commit all files to `main/docs/_entries_drafts/` with an appropriate commit message.
