# Calculation guide

## Question and evidence

How can lesson-planning assumptions be made explicit?

Supplied objective, duration, delivery mode and accessibility needs.

**Status:** SYNTHETIC / RULE-BASED PROTOTYPE | no educational validity claim.

## Design

Analyze objective wording; allocate lesson phases; attach assessment and accessibility prompts; expose review flags.

## Calculation and interpretation

`Allocated phase minutes sum to the requested lesson duration.`

The output is a rule-generated planning blueprint, not a validated lesson. Bloom-verb interpretation, accessibility suitability and assessment alignment still require a teacher’s contextual judgment.

## Evidence table

Worked example — illustrative, not a measured research result. Full precision below is for traceability, not a claim of measurement precision.

| Quantity | Value | Unit / meaning | JSON path |
|---|---:|---|---|
| total minutes: 5+10+10+5 | 30 | unitless | `outputs.total minutes: 5+10+10+5` |
| share of two 10-minute phases | 0.6666666666666666 | unitless | `outputs.share of two 10-minute phases` |

Source: [results/review_examples.json](results/review_examples.json). Values resolve directly from this file when figures are regenerated.

This rule-based lesson planner converts a supplied objective and teaching constraints into a structured lesson blueprint. It allocates time across phases, proposes assessment and accessibility prompts, and flags missing or ambiguous planning inputs. The implementation is transparent and testable, while the resulting activities remain proposals that require contextual instructional review.

## Verification performed in this review

28 existing unittest checks passed. The bundled demonstration executed successfully in this review.

The figure-generation check verifies agreement between the selected source values and SVGs. It does not validate the raw dataset, fitted model, identification assumptions, or external generalization.

```bash
python scripts/build_review_figures.py
python scripts/build_review_figures.py --check
```

For the explicitly illustrative example:

```bash
python scripts/review_examples.py
```

## Implementation map

Follow these functions to inspect each transformation. Validation helpers and private functions remain visible in the linked modules.

| Function | Purpose / documented behavior |
|---|---|
| [`objective_analysis`](src/lesson_design_agent/core.py#L181) | Return matched Bloom evidence and the highest matched cognitive level. |
| [`infer_level`](src/lesson_design_agent/core.py#L223) | Infer the highest matched Bloom level, or None when evidence is absent. |
| [`lesson_blueprint`](src/lesson_design_agent/core.py#L348) | Build an adaptive, deterministic lesson-design scaffold for review. |

## What remains before a stronger research claim

The output is a rule-generated planning blueprint, not a validated lesson. Bloom-verb interpretation, accessibility suitability and assessment alignment still require a teacher’s contextual judgment. A successful software test is not validation of a scientific construct. New experiments should state their split unit, comparator, outcome, uncertainty procedure and failure criteria before examining final test results.
