# AI Agent Personalization Prompt

Give this repository and your transparent portrait path to a coding agent. The agent should follow the workflow below instead of rebuilding the profile from scratch.

---

You are personalizing the GitHub Profile Agent Console starter kit for me.

## Objective

Create a professional English GitHub Profile README that accurately presents who I am, what I focus on, and the strongest projects that support that positioning. Preserve the existing animated console design and generator architecture.

## Rules

1. Read `AGENTS.md`, `README.md`, `docs/QUICK_START.md`, and `profile.schema.json` first.
2. Ask me for any missing factual information. Do not invent experience, affiliations, research, metrics, project ownership, or claims.
3. Help me choose one clear professional headline. Avoid generic labels such as "passionate developer".
4. Curate projects based on the intended positioning, not only recency.
5. Write all public profile copy in concise, professional English.
6. Edit public data only through `profile.config.json` unless a generator bug requires a code fix.
7. Use a transparent head-to-torso PNG. Never copy or commit the source portrait.
8. Generate the profile with:

   ```bash
   npm ci
   npm run generate -- --source /absolute/path/to/my-transparent-portrait.png
   ```

9. Run `npm run check` after generation.
10. Render and inspect desktop/mobile plus dark/light SVG variants. Confirm the portrait is recognizable, the background remains subtle, text fits, and no element overlaps.
11. Run `git status --short` and verify the original portrait is not staged or tracked.
12. Summarize the final positioning, generated files, checks, and any remaining user decisions. Do not push or merge without my approval.

## Information to Collect

- Full display name
- GitHub username
- One professional headline
- University, company, or independent affiliation
- Location
- Current status
- One or two compact About paragraphs
- Primary field, long-term direction, and three short themes
- One to four focus areas
- One to six featured projects with accurate URLs and concise evidence-based descriptions
- Curated tech stack
- Public links only
- Preferred palette: `signal`, `ocean`, or `solar`
- Whether recent public GitHub activity should auto-update
- Absolute local path to the transparent PNG portrait

## Quality Bar

- The first viewport must communicate identity, field, and evidence quickly.
- The hero should feel technical and premium, not badge-heavy or noisy.
- The portrait must remain the highest-contrast object in its panel.
- Project descriptions should explain why each project matters.
- The profile should be credible to collaborators, recruiters, graduate programs, and technical communities.

---

Start by inspecting the repository, then interview me only for information you cannot discover safely.
