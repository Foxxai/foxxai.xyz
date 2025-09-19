# Passwordless Systemd Service Management for Photo Ingest

This guide documents how to enable passwordless control of the `photo_ingest.service` systemd unit for hands-off automation and easy server migration.

## What is a sudoers file?
A sudoers file (`/etc/sudoers`) configures which users can run commands as root (or other users) using `sudo`, and under what conditions (with or without a password, for specific commands, etc.).

**Always use `visudo` to edit the sudoers file for safety.**

## Steps to Enable Passwordless Service Management

1. **Log in as root or a user with sudo privileges.**
2. **Edit the sudoers file safely:**
   ```
   sudo visudo
   ```
3. **Add the following line to allow passwordless control of the photo ingest service:**
   ```
   foxxai ALL=NOPASSWD: /bin/systemctl restart photo_ingest.service, /bin/systemctl start photo_ingest.service, /bin/systemctl stop photo_ingest.service, /bin/systemctl status photo_ingest.service
   ```
   - Replace `foxxai` with your username if different.
   - Adjust the service name if needed for other services.
4. **Save and exit.**

## Migrating to a New Server
- Repeat these steps on the new server for the correct user and service name.
- This ensures your automation remains hands-off and portable.

## Reference
- [Sudoers Manual](https://man7.org/linux/man-pages/man5/sudoers.5.html)
- [Systemd Service Management](https://www.freedesktop.org/software/systemd/man/systemctl.html)
