# Research protocol

## Project

Lesson Design Agent

## Research questions

1. Can explicit instructional constraints improve the consistency and inspectability of machine-assisted lesson planning?
2. How accurately does a transparent objective-verb baseline identify the intended cognitive demand compared with expert judgment?
3. Does adapting lesson phases to cognitive demand reduce obvious objective/activity mismatches?
4. Do contextual review flags help designers notice missing audience, modality, prerequisite, assessment, or accessibility information?
5. How much editing effort is required before a deterministic scaffold becomes an expert-acceptable lesson plan?

## Current baseline

The current implementation is a deterministic lesson-design scaffold. It does not call a language model and does not generate full lesson content.

It currently provides:

- transparent Bloom-style verb evidence
- unknown-state handling when no supported verb is found
- multiple-level detection
- cognitive-demand-specific lesson phase templates
- exact whole-minute allocation
- phase-level design rationale
- assessment-evidence prompts linked to the inferred cognitive demand
- delivery-mode-sensitive accessibility prompts
- review flags for missing or ambiguous design context

## Objective analysis

The baseline selects the highest cognitive level supported by an explicit verb match.

This is intentionally conservative. It does not infer a level from topic words or silently default an unmatched objective to `understand`.

A study should compare these matches with independent expert coding and report disagreement cases.

## Lesson sequence adaptation

The lesson sequence changes across cognitive demands.

Examples:

- **remember** emphasizes retrieval
- **understand** emphasizes explanation and sense-making
- **apply** emphasizes worked examples and guided application
- **analyze** emphasizes decomposition/comparison and evidence
- **evaluate** emphasizes explicit criteria and defended judgment
- **create** emphasizes constraints, construction, critique, and revision

These templates are hypotheses about useful scaffolding, not universal prescriptions.

## Time allocation

Each cognitive level has a provisional phase weighting. The allocation algorithm preserves the exact requested whole-minute total.

For durations of at least four minutes, every phase receives at least one minute. Very short lessons receive a review flag because a four-phase structure may not be realistic.

## Assessment alignment

The system returns a suggested form of evidence matched to the inferred cognitive demand.

This is an alignment prompt, not an automatically generated valid assessment. A designer must still inspect content validity, feasibility, stakes, accessibility, and whether the task actually measures the intended objective.

## Accessibility

The system returns accessibility **prompts**, not pass/fail checks.

Prompts depend partly on delivery mode and any human-supplied accessibility needs. Future evaluation should compare the prompts with expert accessibility review and with the relevant institutional requirements.

## Evidence to collect

Build an expert-reviewed benchmark of lesson briefs that includes:

- topic and audience
- objective
- intended cognitive demand
- delivery mode
- duration
- prerequisite knowledge
- assessment evidence
- accessibility considerations
- expert lesson sequence
- expert rationale

Record inter-rater disagreement rather than collapsing it into a single unquestioned gold label.

## Validation

Compare:

1. the deterministic baseline
2. an unconstrained language-model draft
3. a language-model draft constrained by the same design schema
4. expert-designed reference plans

Use separate ratings for objective interpretation, activity fit, time realism, assessment alignment, accessibility planning, pedagogical rationale, and editing effort.

## What counts as a useful result

A useful result shows where explicit structure helps designers and where it creates false confidence, unnecessary rigidity, or additional editing work.

## Threats to validity

Bloom verb lists are only proxies for cognitive demand. Objectives can contain several actions, hide prerequisites, or use verbs that are ambiguous across disciplines.

Lesson timing depends on learner readiness, class size, modality, technology, teacher expertise, content complexity, and local constraints.

Accessibility needs cannot be reduced to a universal checklist, and instructional alignment requires subject-matter judgment that this prototype does not possess.
