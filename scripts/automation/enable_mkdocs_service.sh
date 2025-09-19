#!/bin/bash
# Enable and start the MkDocs local server service for full automation
sudo systemctl enable mkdocs_dev.service
sudo systemctl start mkdocs_dev.service
