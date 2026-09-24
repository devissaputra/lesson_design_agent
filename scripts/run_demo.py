import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lesson_design_agent.core import lesson_blueprint


plan = lesson_blueprint(
    topic="Operational risk analysis",
    objective="Analyze operational risks and justify a response recommendation.",
    minutes=90,
    audience="early-career operations analysts",
    delivery_mode="hybrid",
    prior_knowledge="basic probability and process mapping",
    class_size=24,
    assessment_mode="case analysis",
    accessibility_needs=[
        "captions for video",
        "screen-reader compatible digital materials",
    ],
)

print("Topic:", plan["topic"])
print("Objective:", plan["objective"])
print("Objective level:", plan["objective_level"])
print("Objective evidence:", plan["objective_evidence"])
print("Sequence:")
for stage in plan["sequence"]:
    print(
        f"  - {stage['phase']}: {stage['minutes']} min"
        f" | {stage['rationale']}"
    )
print("Assessment prompt:", plan["assessment_prompt"]["suggested_evidence"])
print("Accessibility prompts:")
for prompt in plan["accessibility_prompts"]:
    print("  -", prompt)
print("Review flags:", plan["review_flags"] or ["none"])
print("Design status:", plan["design_status"])
print("Note: this is a deterministic design scaffold, not generated lesson content.")
