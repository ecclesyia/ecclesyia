# Contributing

Contributions should improve setup reliability, rendering quality, accessibility, documentation, or cross-platform behavior without weakening portrait privacy.

## Development

```bash
npm install
npm run check
```

Use a transparent portrait that you have permission to process for local visual testing. Never add someone else's source portrait to a pull request.

Generated visual changes should be checked in desktop/mobile and dark/light modes. Keep configuration backward-compatible when possible and document any new public field in both `profile.schema.json` and `docs/CUSTOMIZATION.md`.
