---
description: "Incident response and DFIR organised around questions, artifacts and defensible conclusions."
---

# Incident Response & DFIR

`INVESTIGATE // RECONSTRUCT THE EVENT`

An investigation needs an account of what happened and a visible route back to the evidence. This section is for incident response, forensic workflows, timelines and threat investigation: the work of testing an explanation against the artifacts available.

## Frame the investigation

Begin with a bounded question: which account acted, what executed, or how two events relate. Record the time window, systems in scope and gaps in collection before expanding the narrative.

Keep three things distinct in the working account:

- **Observation:** what the artifact actually contains, with its provenance.
- **Interpretation:** what that observation supports and which assumptions it needs.
- **Open question:** what would strengthen, contradict or change the interpretation.

That separation is the editorial standard for investigations here. Timelines should preserve source timestamps and explain any normalisation; reports should make competing explanations visible.

## Follow the work

Use [Reference](../reference/README.md) for artifact fields and interpretation boundaries. Move to [Detect](../detect/README.md) when the investigation produces a behaviour worth looking for elsewhere. Use [Build](../build/README.md) when a disputed assumption needs an isolated experiment.
