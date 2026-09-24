import re

BLOOM_ORDER = ["remember", "understand", "apply", "analyze", "evaluate", "create"]
VERBS = {
    "remember": "define",
    "understand": "explain",
    "apply": "apply",
    "analyze": "analyze",
    "evaluate": "justify",
    "create": "design",
}


def infer_level(objective: str) -> str:
    """Infer a simple Bloom level from explicit action verbs."""
    words = set(re.findall(r"[a-z]+", objective.lower()))
    for level in reversed(BLOOM_ORDER):
        if VERBS[level] in words:
            return level
    return "understand"


def _allocate_minutes(total: int, shares=(0.15, 0.25, 0.35, 0.25)) -> list[int]:
    raw = [total * share for share in shares]
    allocated = [int(value) for value in raw]
    remainder = total - sum(allocated)
    order = sorted(
        range(len(raw)),
        key=lambda index: (raw[index] - allocated[index], -index),
        reverse=True,
    )
    for index in order[:remainder]:
        allocated[index] += 1
    return allocated


def lesson_blueprint(topic: str, objective: str, minutes: int = 60) -> dict:
    """Build a deterministic lesson sequence for review by a learning designer."""
    if not topic.strip() or not objective.strip():
        raise ValueError("topic and objective must not be empty")
    if minutes <= 0:
        raise ValueError("minutes must be positive")

    level = infer_level(objective)
    durations = _allocate_minutes(minutes)
    labels = (
        "activate prior knowledge",
        "guided example",
        "learner practice",
        "feedback and reflection",
    )
    return {
        "topic": topic,
        "objective": objective,
        "level": level,
        "sequence": list(zip(labels, durations)),
        "accessibility_checks": [
            "plain language instructions",
            "alternative text for meaningful visuals",
            "keyboard accessible interaction",
            "multiple ways to demonstrate learning",
        ],
    }
