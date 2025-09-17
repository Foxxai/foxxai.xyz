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

## Notes
- Update paths in the service file if you move your project.
- Document any additional automation scripts here as you add them.
