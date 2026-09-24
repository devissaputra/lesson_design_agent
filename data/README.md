# Data documentation

## Included data

`sample.csv` contains synthetic lesson-design briefs used to demonstrate the repository schema. It contains no learner records and no empirical outcomes.

## Current schema

- `topic`: lesson topic
- `objective`: intended observable learner performance
- `minutes`: total lesson duration in whole minutes
- `audience`: intended learner group
- `delivery_mode`: for example online, hybrid, or in-person
- `prior_knowledge`: prerequisite knowledge or skill assumed by the design
- `class_size`: expected participant count
- `assessment_mode`: intended way evidence of learning will be collected
- `accessibility_needs`: known design needs, separated by semicolons in the CSV example

## Why context matters

The same objective can require a different lesson design for a different audience, duration, delivery mode, or prior-knowledge profile.

The current code therefore treats missing context as a review issue rather than pretending a topic and objective are sufficient to finalize a lesson.

## Objective analysis

The baseline uses a transparent Bloom-style verb lexicon to identify explicit cognitive-demand evidence in an objective.

It does **not** claim to understand the full semantic meaning of the objective.

If no supported verb is found, the cognitive level is left unknown and the plan receives an `objective_level_unknown` review flag.

If verbs from several levels appear, the highest matched level is used to select the provisional lesson pattern and a `multiple_cognitive_levels_detected` flag is added for designer review.

## Accessibility fields

Accessibility needs are design context supplied by a human. The software does not diagnose disability or infer needs from learner data.

The resulting accessibility output is a set of prompts for review, not an automated accessibility certification.

## Do not commit

Do not commit personally identifiable learner information, disability or health records, private accommodation documents, raw student work, proprietary course content, or licensed materials that prohibit redistribution.

## Design brief requirement

For real design work, record the audience, objective, duration, delivery mode, prerequisites, assessment approach, known accessibility needs, available technology/materials, and any institutional constraints that materially affect the lesson.
