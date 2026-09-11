---
description: "Choose a route through the archive and understand what its evidence labels mean."
---

# Start Here

`READER BRIEFING`

Start with the question you need to answer. The archive is arranged around investigation, detection and engineering work, with references for the details you need to look up repeatedly.

| Your question | Route | Useful output |
|---|---|---|
| What happened, and what supports that account? | [Investigate](../investigate/README.md) | A timeline with evidence and uncertainty attached |
| How would we recognise this behaviour? | [Detect](../detect/README.md) | A hypothesis, telemetry requirements and validation criteria |
| How can I reproduce or engineer this? | [Build](../build/README.md) | An experiment or design with explicit boundaries |
| What does this field, artifact or command mean? | [Reference](../reference/README.md) | A concise answer with applicability and caveats |
| What is worth examining next? | [Dispatches](../dispatches/README.md) | A focused observation, tool assessment or research question |

## A first read

Start with [Evidence of Program Execution](../investigate/dfir/evidence-of-program-execution.md). It asks what supports the claim that a Windows program ran, then separates file presence, artifact references, evidence consistent with execution and directly recorded process creation.

Its **SOURCE VALIDATED** label means the interpretations were checked against cited sources within the stated version and configuration limits. It does not mean every artifact was reproduced in a fresh lab. Use the corroboration workflow, then check what telemetry your own environment actually collected.

## Read the evidence label

**LAB VALIDATED** means the described procedure or result was reproduced in an authorised lab. Read the environment and evidence to see exactly what was tested; the label does not extend to other versions or deployments.

**SOURCE VALIDATED** means the claims were checked against cited sources. It does not mean the procedure was reproduced end to end.

**FIELD NOTE** identifies observation, analysis or opinion. It should tell you whose observation it is, its context and what remains uncertain.

Published dates describe release history. Last verified dates describe the most recent technical check within the stated scope. Neither guarantees that a method fits your environment today.

## Notes in the margin

**K-2AI** callouts highlight an interpretation trap or a practical check; they are editorial assistance, not additional evidence. **DEATH STAR LAB CAPTURE** prompts identify a future screenshot that would help explain the method. A prompt is not a completed experiment or an existing image.

## Carry the reasoning with the result

When using a technical article, keep its prerequisites, evidence and limitations together. A command without the expected output is difficult to assess; an output without interpretation is easy to overread. If an article leaves an important question unresolved, treat it as unresolved.

[About Darkcybe and K-2AI](../about/README.md) explains authorship and editorial assistance.
