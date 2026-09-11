---
description: "Detection engineering and hunting with explicit telemetry, hypotheses and test boundaries."
---

# Detection Engineering & Hunting

`DETECT // DEFINE THE SIGNAL`

A detection article should explain the behaviour it is looking for, the data it needs and how its result was assessed. This section covers detection logic, telemetry design and threat hunting with those questions kept together.

## Write the hypothesis first

Describe the behaviour in plain language before choosing a query language. Then name the event sources, fields and collection assumptions required to observe it. Keep the analytical idea separate from the syntax used by a particular platform.

A useful review asks:

- What should match, and what similar legitimate activity should not?
- Which missing fields, collection gaps or environment differences would change the result?
- What evidence supports the claimed coverage, and what remains untested?
- What should an analyst examine after a match?

Hunts belong here when they have a question, a search method and an account of the result, including inconclusive results. A quiet query is not a complete investigation narrative.

## Connect the signal to a decision

[Investigate](../investigate/README.md) provides the evidence context behind a hypothesis. [Build](../build/README.md) covers the lab and instrumentation needed to exercise it. Durable field and query explanations belong in [Reference](../reference/README.md).
