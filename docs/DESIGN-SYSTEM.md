# Darkcybe 3.0 design system

## Identity and reading experience

A terminal into the Death Star / Holonet Operations Centre: cyber-noir, precise, quiet. The reader comes for useful cybersecurity reasoning. Use the operations-centre character in the masthead, short section labels and occasional dry phrasing; keep article titles and prose descriptive.

The homepage opens with `DARKCYBE // HOLONET TERMINAL` and `IMPERIAL SECURITY ARCHIVE`. Native cards expose the five reader journeys. Start Here explains the evidence model. Default GitBook content width keeps prose readable. The eight initial reader pages establish the publication's intent; they are not a claim that the historical corpus has been refreshed.

## Palette and typography

These are proposed GitBook UI settings, not Markdown theme keys or an implemented skin.

| Role | Target | Use |
|---|---|---|
| Charcoal | `#14171B` | Dark-first background |
| Gunmetal | `#252B33` | Panels and secondary surfaces |
| Pale neutral | `#E6E8EB` | Main text |
| Muted neutral | `#AAB2BD` | Secondary text, subject to contrast checks |
| Imperial red | `#B83A42` | Restrained brand accent; never long body text |
| Amber | `#D8A34A` | Meaningful caution or verification limits |

Use GitBook's readable prose font. Reserve monospace for commands, paths, versions and short terminal labels. Retain a light-mode option where available. Check contrast, keyboard focus and mobile readability in both modes during the later GitBook bootstrap. Native hint colours remain semantic; do not misuse a danger block merely to obtain red.

Suggest panel rhythm through headings, whitespace and native cards. No animated cursor, scan-line overlay or artificial telemetry. A subtle static motif may be considered later only through supported GitBook assets/settings and only if it preserves readability. A02 introduces no decorative image requirement.

## Voice, terminology and roles

- Darkcybe is the author/publisher. Use plain first-person statements only when Darkcybe's supplied experience supports them.
- K-2AI is secondary: `K-2AI // HOLONET EDITORIAL SYSTEM`; compact assistance credit: `K-2AI // HOLONET`.
- Use Investigate, Detect, Build, Reference and Dispatches as reader routes. "Archive" describes the knowledge collection, not an assertion that every page is current.
- Prefer "observation", "inference", "limitation" and "not tested" over inflated certainty. Do not invent alert counts, operational status, clearance levels or classified-source implications.

## Article identity and evidence

Use a compact two-column Markdown table near the beginning of a substantive article. Keep the title human-readable; labels are the terminal detail.

| Field | Authoring value |
|---|---|
| AUTHOR | DARKCYBE |
| EDITORIAL / RESEARCH ASSISTANCE | K-2AI // HOLONET, only when applicable |
| VALIDATION | Select one evidence state below; omit while unassessed |
| PUBLISHED | Actual publication date, `YYYY-MM-DD`; pending in drafts |
| LAST VERIFIED | Actual technical review date, `YYYY-MM-DD`, or not yet verified |

- **LAB VALIDATED:** the described procedure/result was reproduced in an authorised lab. Name the environment, versions, tester and evidence, and bound the claim to what was exercised. Never imply K-2AI performed tests without corresponding evidence.
- **SOURCE VALIDATED:** current claims checked against linked authoritative sources, with the reviewed scope/date. Explicitly state that end-to-end reproduction was not performed where relevant.
- **FIELD NOTE:** attributed observation, analysis or opinion with its context and uncertainties. It is not an escape hatch for unsupported technical claims.

Labels describe evidence, not confidence scores. Foundational landing pages need no validation badge. Draft status and technical validation are separate; copying a template earns neither verification nor publication. A documentation CI pass never establishes LAB VALIDATED.

## Article shape and native components

Use only the sections that help the article: TL;DR, why it matters, environment, methodology, artifact interpretation, limitations, takeaways and references. Published/verified dates and evidence context should survive any shortening. The four [templates](../templates/technical-guide.md) are authoring references, excluded from `SUMMARY.md` along with this design document and repository machinery.

Use native card tables for route choices, hints for consequential context, tabs for actual alternatives and steppers for substantial sequential instructions. Use ordinary tables for comparisons. Do not hide prerequisites or critical limitations in collapsible sections. Links within this single content space are relative file paths.

K-2AI callouts use an `info` hint with the full editorial-system label and a short, specific contribution. Use them occasionally, not on every section. Do not use them to manufacture a second authorial voice or repeat the article summary.

## Diagrams and screenshots

Use Mermaid fenced blocks for flows, trust boundaries, timelines and evidence relationships where they clarify the reasoning. Keep labels literal, diagrams small and colours optional. Put a prose explanation alongside the diagram; a labelled dotted edge can represent uncertainty without depending on colour. Avoid custom Mermaid themes, scripts and elaborate dashboard diagrams. Rendering must be checked later in GitBook.

Screenshots must demonstrate a relevant observation. Crop to the useful region; supply alt text, caption, version and provenance. Use sanitised lab images with no credentials, customer/case details, private identifiers or runtime information. Keep copyable commands and important results in text. Do not use a screenshot as proof of a wider test than it shows.

`assets/` is reserved for deliberately reviewed public assets. GitBook UI uploads may later use its native `.gitbook/assets/` directory; do not invent a parallel upload system.

## Prohibited

No hooded-hacker imagery, franchise character collages, ornamental weapons, fan-site roleplay, fake operational telemetry, flashing effects, full-page monospace prose, filler or fabricated experience. No CSS/JS frontend, custom rendering pipeline, unsupported styling attributes or theme settings inside `.gitbook.yaml`. No bulk legacy import, redirects or live GitBook changes in A02.

## GitBook basis and review boundary

Reviewed 2026-09-11: GitBook's [AI assistant guidance](https://gitbook.com/docs/docs-as-code/ai-coding-assistants-and-skillmd), [writing skill](https://github.com/GitbookIO/gitbook-skills/blob/main/skills/write-docs/SKILL.md), [block syntax](https://github.com/GitbookIO/gitbook-skills/blob/main/skills/write-docs/references/blocks.md), [configuration grammar](https://github.com/GitbookIO/gitbook-skills/blob/main/skills/write-docs/references/configuration.md) and [site configuration skill](https://github.com/GitbookIO/gitbook-skills/blob/main/skills/configure-site/SKILL.md).

The explicit A02 brief governs the root-level single-space layout and defers site creation, sync and preview. Current GitBook guidance describes site-wide mapping through `gitbook-docs.yaml`; that UI-generated mapping belongs to the later bootstrap. The requested `.gitbook.yaml` here selects only root, homepage and summary. `SUMMARY.md` uses native groups; ABOUT separates the final page from DISPATCHES.

Local validation checks structure only. Later render review must inspect card wrapping, navigation grouping, hint appearance, tables, contrast, mobile layout and the exclusion of authoring files from the reader tree. The A02 review question is: **Does this feel like the new Darkcybe?**
