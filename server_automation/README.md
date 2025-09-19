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
- `mkdocs_rebuild.service`: Systemd unit file to automatically rebuild the MkDocs static site after photo processing.
- Uses `.venv-mkdocs` for all MkDocs dependencies.
- To enable and start the service:
  ```bash
  sudo cp server_automation/mkdocs_rebuild.service /etc/systemd/system/
  sudo systemctl daemon-reload
  sudo systemctl enable mkdocs_rebuild.service
  sudo systemctl start mkdocs_rebuild.service
  ```
- To check status:
  ```bash
  sudo systemctl status mkdocs_rebuild.service
  ```

### Customization & Portability
- Update `WorkingDirectory`, `ExecStart`, and `User` in the service file for your environment.
- Ensure `.venv-photo` and `.venv-mkdocs` are present and all requirements are installed.
- SELinux and firewall rules may need to be updated for file access and automation.
- Document any changes in this README for future migrations.

### Troubleshooting
- Check logs with `journalctl -u photo_ingest.service` and `journalctl -u mkdocs_rebuild.service`
- Ensure all Python and MkDocs dependencies are installed in `.venv-photo` and `.venv-mkdocs`
- Verify file permissions for the service user

---

Add additional services and document them here as you expand automation.
