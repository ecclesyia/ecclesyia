# Agent Instructions

This repository generates a public GitHub Profile README from structured configuration and a private portrait source.

## Source of Truth

- Edit public profile content in `profile.config.json`.
- Generate assets with `npm run generate -- --source /absolute/path/to/portrait.png`.
- Do not hand-edit files in `assets/hero/`; they are generated.
- A generated profile `README.md` contains a notice at the top. Regenerate it instead of manually changing generated sections.

## Privacy

- Never copy or commit the original portrait.
- Prefer a portrait path outside the repository.
- Only generated ASCII SVG assets may be committed.
- Never add credentials, private email addresses, or unpublished project information to the profile without explicit approval.

## Quality Checks

Run these commands after changes:

```bash
npm run check
```

For visual changes, render and inspect desktop/mobile plus dark/light SVG variants.

## GitHub Profile Constraints

- Keep the hero readable at GitHub's profile width.
- Preserve `<picture>` sources for responsive dark/light variants.
- Keep generated activity inside its bounded marker block.
- Use new hash-based asset filenames when the portrait or configuration changes to avoid GitHub image caching.
