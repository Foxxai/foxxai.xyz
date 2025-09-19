# Travelogue Ingest Workflow

This directory is dedicated to the ingestion, processing, and automation of academic travelogue photos for the ScholarFlow project.

## Structure

- `new_images/`: Place new photos here for processing.
- `processed/`: Archive for original images after processing.
- `captions/`: Stores YAML caption/metadata files (to be consolidated).
- `logs/`: Error and workflow logs.

## Workflow

- Photos placed in `new_images/` are automatically processed (resized, thumbnailed, captioned).
- Processed images are moved to `processed/` and live gallery asset directories.
- Captions and metadata are generated and stored in `captions/`.
- Errors and process logs are written to `logs/`.

## Integration

- This ingest folder is managed by a Python automation script and a systemd service for robust, SELinux-friendly operation.
- All triggers and integration points are documented in the project root README.

Refer to the project root README for a list of all triggers and ingest folders.
