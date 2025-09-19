# Server Automation Setup

This directory contains automation scripts and service definitions for running background jobs on your local server.

## Blog Index Watcher
- `blogs_watch.service`: Systemd unit file to run the blog watcher script automatically on boot.
- Ensure your Python environment is set up and dependencies (e.g., watchdog) are installed in `.venv`.
- To enable and start the service:
  ```bash
  sudo cp server_automation/blogs_watch.service /etc/systemd/system/
  sudo systemctl daemon-reload
  sudo systemctl enable blogs_watch
  sudo systemctl start blogs_watch
  ```
- To check status:
  ```bash
  sudo systemctl status blogs_watch
  ```

## Research Travelogue Photo Ingest
- `photo_ingest.service`: Systemd unit file to automate photo processing for the Research Travelogue section.
- Uses `.venv-photo` for all Python dependencies.
- To enable and start the service:
  ```bash
  sudo cp server_automation/photo_ingest.service /etc/systemd/system/
  sudo systemctl daemon-reload
  sudo systemctl enable photo_ingest.service
  sudo systemctl start photo_ingest.service
  ```
- To check status:
  ```bash
  sudo systemctl status photo_ingest.service
  ```

## MkDocs Rebuild Automation
  ```bash
  sudo cp server_automation/mkdocs_rebuild.service /etc/systemd/system/
  sudo systemctl daemon-reload
  sudo systemctl enable mkdocs_rebuild.service
  sudo systemctl start mkdocs_rebuild.service
  ```
  ```bash
  sudo systemctl status mkdocs_rebuild.service
  ```

## Research Travelogue Gallery Automation

### How it works
- Place new images in `travelogue_ingest/new_images/`.
- The image processing script (`scripts/gallery/process_images.py`) will:
  - Detect new images and process them (create thumbnails, optimize full images).
  - Move processed images to `docs/assets/travelogue/full/` and `docs/assets/travelogue/thumbnails/`.
  - Update the gallery markdown (`docs/travelogue/index.md`) and metadata.
  - Automatically stage, commit, and push images and gallery updates to `main`.
  - Trigger a MkDocs rebuild.

### Verification and CI
- The workflow runs a verification script (`scripts/automation/verify_gallery_images.py`) before deployment.
- This script checks that every image referenced in the gallery markdown exists and is tracked by git.
- If any images are missing or untracked, deployment fails—preventing broken galleries online.

### No manual steps required
- You do not need to manually move, stage, or commit images or gallery updates.
- Simply add new images to `travelogue_ingest/new_images/` and the automation will handle everything.

## Docs Change Watcher & Automated Rebuild
- `watch_docs_and_rebuild.py`: Watches for changes in `docs/` (excluding underscored directories) and triggers a MkDocs rebuild automatically.
- To run as a service or background process, use a systemd unit or tmux/screen session.

## Passwordless Service Management
- For hands-off automation, set up passwordless sudo for service management:
  ```
  sudo visudo -f /etc/sudoers.d/foxxai-systemd
  ```
  Add lines like:
  ```
  foxxai ALL=NOPASSWD: /bin/systemctl start mkdocs_dev.service, /bin/systemctl stop mkdocs_dev.service
  foxxai ALL=NOPASSWD: /bin/systemctl restart photo_ingest.service, /bin/systemctl start photo_ingest.service, /bin/systemctl stop photo_ingest.service, /bin/systemctl status photo_ingest.service
  foxxai ALL=NOPASSWD: /bin/systemctl restart mkdocs_rebuild.service, /bin/systemctl restart photo_ingest.service, /bin/systemctl restart mkdocs_dev.service
  ```

## Service Overview
- `photo_ingest.service`: Automates photo processing and gallery updates.
- `mkdocs_rebuild.service`: Triggers a site rebuild after photo ingest or docs changes.
- `mkdocs_dev.service`: Serves the site locally for development.
- `blogs_watch.service`: Watches and automates blog index updates.

## SELinux Troubleshooting
- If using SELinux, see `mkdocs_dev.md` for policy setup and troubleshooting.

---

Add additional services and document them here as you expand automation.
