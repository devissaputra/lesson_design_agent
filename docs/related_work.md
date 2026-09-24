# Related work and methodological context

Lesson Design Agent is an original deterministic implementation. Its current design is informed by established instructional-design ideas, but the repository does not claim to reproduce or validate any one framework.

## Learning objectives and Bloom-style cognitive demand

Carnegie Mellon University's Eberly Center describes learning objectives as student-centered, actionable, and measurable, and presents Bloom's taxonomy as a practical way to think about the cognitive demand of objectives.

- Learning objectives: https://www.cmu.edu/teaching/designteach/syllabus/newcourse/learningobjectives.html
- Bloom's taxonomy: https://www.cmu.edu/teaching/designteach/design/bloomsTaxonomy.html

The current code uses a transparent verb lexicon inspired by this kind of objective-writing practice.

It does **not** assume that a verb alone fully determines cognitive demand.

## Alignment

The Eberly Center also emphasizes alignment among learning objectives, instructional activities, and assessment.

This repository reflects that relationship by keeping three things visible:

1. the objective evidence used by the baseline
2. the lesson phases selected from that evidence
3. the suggested form of assessment evidence

The current implementation is only a design scaffold. Subject-matter experts and learning designers must still decide whether the activity and assessment genuinely align with the intended learning outcome.

## Universal Design for Learning

CAST's Universal Design for Learning Guidelines 3.0 organize design considerations around engagement, representation, and action/expression.

- CAST UDL Guidelines 3.0: https://udlguidelines.cast.org/
- CAST downloads and citation information: https://udlguidelines.cast.org/more/downloads/

The accessibility layer in this repository is intentionally described as a set of **prompts**. It is not a UDL scoring tool and does not claim to certify that a lesson is accessible.

## Relationship to generative lesson design

The current baseline does not call a language model.

Its research value is as a transparent control condition for future studies comparing:

- deterministic structured scaffolds
- unconstrained generative lesson drafts
- generative drafts constrained by the same schema
- expert-designed lesson plans

This separation makes it possible to study whether generative systems add genuine design value beyond formatting and fluent prose.
