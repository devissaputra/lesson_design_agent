# Analytic system card

## System

Lesson Design Agent

## Purpose

A deterministic instructional-design scaffold that makes objective interpretation, lesson sequencing, time allocation, assessment evidence, accessibility prompts, and missing design context visible for human review.

## Current maturity

Working research prototype.

The bundled briefs are synthetic and demonstrate the software path. They do not establish that the templates improve learning outcomes or outperform expert lesson design.

## Inputs

The main `lesson_blueprint()` function accepts:

- topic
- learning objective
- duration in whole minutes
- audience
- delivery mode
- prior knowledge
- class size
- assessment mode
- known accessibility needs

Only topic, objective, and duration are required to execute, but missing contextual fields generate review flags.

## Objective analysis

The system matches explicit verbs against a transparent Bloom-style lexicon.

It returns:

- highest matched cognitive level
- matched verb evidence
- all matched cognitive levels

When no supported verb is found, the level remains unknown rather than defaulting to a fabricated value.

When more than one cognitive level is present, the highest matched level selects the provisional template and a review flag records the ambiguity.

## Lesson sequence

Each supported cognitive level has its own four-phase lesson pattern and provisional time weighting.

The code preserves the exact requested duration.

The templates are inspectable design hypotheses rather than learned policies or universal pedagogical rules.

## Assessment output

The system proposes a type of evidence appropriate to the provisional cognitive demand.

This output is an alignment prompt, not a generated validated assessment.

## Accessibility output

The system generates accessibility prompts based on delivery mode and any human-supplied accessibility needs.

It does not test a website, inspect media files, verify legal compliance, or infer disability.

## Review flags

Current flags can identify:

- unknown objective level
- multiple cognitive levels
- very short duration
- missing audience
- missing delivery mode
- missing prior knowledge
- missing assessment mode
- missing accessibility context

These flags are prompts for design review, not errors or automatic rejection rules.

## Main limitations

The current baseline:

- does not understand subject matter
- does not generate full lesson content
- does not verify factual accuracy
- does not validate assessment quality
- does not certify accessibility
- does not model learner performance
- does not optimize timing from empirical outcomes
- does not call a language model

## Evidence needed before real use

Build an expert-reviewed benchmark and measure objective interpretation, sequence fit, time realism, assessment alignment, accessibility planning, designer agreement, and revision effort.

Any future generative version should be compared against this transparent baseline rather than evaluated only on fluency.

## Human oversight

A learning designer or instructor remains responsible for the final objective, activities, examples, assessment, accessibility decisions, content accuracy, and local curriculum requirements.
