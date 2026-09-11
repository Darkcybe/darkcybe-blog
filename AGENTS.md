# Publication contract

- Darkcybe is the author and publisher. K-2AI is the editorial/research assistant, identified as `K-2AI // HOLONET EDITORIAL SYSTEM` when useful.
- AI output is never autonomously published. Work on `codex/*` branches; Darkcybe's PR review is the publication boundary. Do not merge or publish without explicit authority.
- Never expose private Obsidian material, customer/case information, credentials, Holonet secrets or private runtime information. Only deliberately selected, sanitised public material belongs here.
- Never fabricate testing, field experience, citations or certainty. Distinguish observation, source claims, inference and unknowns; source current technical claims.
- Follow [the design system](docs/DESIGN-SYSTEM.md). Templates are authoring references, not mandatory section checklists or published pages.
- Before GitBook-specific edits, read the current [official writing skill](https://github.com/GitbookIO/gitbook-skills/blob/main/skills/write-docs/SKILL.md) and relevant references. Preserve useful GitBook-native Markdown. Do not invent CSS/JS styling or a frontend.
- Keep implementation deliberately simple. Run `python3 scripts/validate_publication.py`, `python3 -m unittest discover -s tests` and `git diff --check` before handing off a PR. Structural checks do not prove technical accuracy or GitBook rendering.
