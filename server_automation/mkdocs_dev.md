# MkDocs Local Server Automation

This document describes how to set up and manage the MkDocs local development server as a systemd service for persistent site serving and automation.

## Service File: `mkdocs_dev.service`

- Located in `server_automation/mkdocs_dev.service`.
- Runs the MkDocs server using the Python virtual environment in `.venv`.
- Serves the site on `127.0.0.1:8000` for local-only development and testing.
- Uses explicit Python invocation for SELinux compatibility:

  ```ini
  ExecStart=/home/foxxai/Repos/foxxai.xyz/.venv/bin/python3 /home/foxxai/Repos/foxxai.xyz/.venv/bin/mkdocs serve --dev-addr=127.0.0.1:8000
  ```

### Installation Steps

1. Copy the service file to systemd:

   ```bash
   sudo cp server_automation/mkdocs_dev.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable mkdocs_dev
   sudo systemctl start mkdocs_dev
   ```

2. If SELinux is enforcing, create and apply a policy module:

   ```bash
   sudo ausearch -c 'mkdocs' --raw | audit2allow -M mkdocs_local_server
   sudo semodule -i mkdocs_local_server.pp
   ```

3. Check the status:

   ```bash
   sudo systemctl status mkdocs_dev
   ```

4. To verify autostart on reboot:

   ```bash
   systemctl is-enabled mkdocs_dev   # should return 'enabled'
   sudo reboot
   # After reboot, check:
   sudo systemctl status mkdocs_dev
   ```

### Notes

- Update paths in the service file if you move your project directory.
- Ensure `.venv` is activated and MkDocs is installed (`pip install mkdocs mkdocs-material`).
- For SELinux-enabled systems, see troubleshooting steps in this directory if you encounter permission denials.

## Troubleshooting

- If the service fails to start, check logs with:

  ```bash
  journalctl -u mkdocs_dev
  ```

- For SELinux denials, see `selinux_policy.md` in this directory.

---

Document any further automation or service changes here for future reference.
