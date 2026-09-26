# Calculation reading guide: ../CALCULATIONS.md (repository root).
# Allocated phase minutes sum to the requested lesson duration.
# The output is a rule-generated planning blueprint, not a validated lesson. Bloom-verb interpretation, accessibility suitability and assessment alignment still require a teacher’s contextual judgment.

import math
import re
from collections.abc import Iterable


BLOOM_ORDER = [
    "remember",
    "understand",
    "apply",
    "analyze",
    "evaluate",
    "create",
]

BLOOM_VERBS = {
    "remember": {
        "define",
        "identify",
        "label",
        "list",
        "name",
        "recall",
        "recognize",
        "state",
    },
    "understand": {
        "classify",
        "describe",
        "discuss",
        "explain",
        "interpret",
        "paraphrase",
        "summarize",
    },
    "apply": {
        "apply",
        "calculate",
        "demonstrate",
        "execute",
        "implement",
        "solve",
        "use",
    },
    "analyze": {
        "analyze",
        "compare",
        "contrast",
        "differentiate",
        "examine",
        "organize",
        "deconstruct",
    },
    "evaluate": {
        "assess",
        "critique",
        "defend",
        "evaluate",
        "judge",
        "justify",
        "recommend",
    },
    "create": {
        "build",
        "compose",
        "construct",
        "create",
        "design",
        "develop",
        "formulate",
        "produce",
        "revise",
    },
}

LEVEL_TEMPLATES = {
    "remember": {
        "shares": (0.20, 0.25, 0.35, 0.20),
        "phases": (
            ("activate prior knowledge", "connect the target facts or terms to what learners already know"),
            ("concise explanation", "introduce the essential content with examples and non-examples"),
            ("retrieval practice", "practice recalling and recognizing the target knowledge"),
            ("feedback and reflection", "check recall, correct misconceptions, and summarize key points"),
        ),
        "assessment": "Use a brief retrieval task that directly samples the facts, terms, or distinctions named in the objective.",
    },
    "understand": {
        "shares": (0.15, 0.30, 0.35, 0.20),
        "phases": (
            ("activate prior knowledge", "surface relevant prior ideas and likely misconceptions"),
            ("model meaning", "explain the concept with examples, representations, and relationships"),
            ("guided sense-making", "have learners classify, explain, summarize, or interpret examples"),
            ("feedback and reflection", "check explanations and ask learners to connect ideas in their own words"),
        ),
        "assessment": "Ask learners to explain, summarize, classify, or interpret the target concept in a way that makes their understanding observable.",
    },
    "apply": {
        "shares": (0.10, 0.30, 0.40, 0.20),
        "phases": (
            ("activate prerequisites", "confirm the prerequisite procedure, rule, or concept"),
            ("worked example", "model how the procedure is applied and make decision points visible"),
            ("guided application", "practice applying the method with fading support"),
            ("independent transfer and feedback", "apply the method to a new case and review the result"),
        ),
        "assessment": "Use a novel but bounded task that requires learners to apply the procedure or principle without simply copying the worked example.",
    },
    "analyze": {
        "shares": (0.10, 0.25, 0.45, 0.20),
        "phases": (
            ("orient to criteria", "activate the concepts or criteria needed to inspect relationships"),
            ("model analysis", "demonstrate decomposition, comparison, or relationship mapping"),
            ("guided analysis", "analyze a case with prompts that make reasoning visible"),
            ("independent analysis and critique", "analyze a new case, justify relationships, and receive feedback"),
        ),
        "assessment": "Use a case, dataset, argument, or process that requires learners to separate parts, compare relationships, and justify the analysis with evidence.",
    },
    "evaluate": {
        "shares": (0.10, 0.25, 0.40, 0.25),
        "phases": (
            ("establish criteria", "make the standards for judgment explicit"),
            ("model evidence-based judgment", "show how evidence is weighed against the criteria"),
            ("guided evaluation", "evaluate a case and defend a judgment with evidence"),
            ("defend and revise", "present, challenge, and revise a judgment after feedback"),
        ),
        "assessment": "Ask learners to judge an option, claim, or solution against explicit criteria and defend the judgment with evidence.",
    },
    "create": {
        "shares": (0.10, 0.20, 0.50, 0.20),
        "phases": (
            ("frame constraints", "clarify the problem, audience, criteria, and constraints"),
            ("study exemplars and strategies", "inspect relevant examples and make design choices visible"),
            ("iterative construction", "build, test, and refine an artifact or solution"),
            ("critique and revision", "use feedback and criteria to improve the artifact and explain key decisions"),
        ),
        "assessment": "Require a new artifact, plan, model, or solution that satisfies explicit constraints, plus a short rationale for the major design decisions.",
    },
    "unknown": {
        "shares": (0.15, 0.25, 0.40, 0.20),
        "phases": (
            ("clarify the objective", "identify the observable learner performance before committing to an activity pattern"),
            ("surface prerequisite knowledge", "check what learners need before attempting the target performance"),
            ("provisional practice", "use a low-risk activity while the intended cognitive demand is clarified"),
            ("review and refine", "confirm the objective, evidence of learning, and next design decision"),
        ),
        "assessment": "Clarify the observable learner performance before selecting an assessment task.",
    },
}


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z]+", text.lower())


def _candidate_bases(token: str) -> set[str]:
    candidates = {token}

    if token.endswith("ies") and len(token) > 3:
        candidates.add(token[:-3] + "y")
    if token.endswith("ying") and len(token) > 5:
        candidates.add(token[:-4] + "y")
    if token.endswith("ing") and len(token) > 4:
        stem = token[:-3]
        candidates.add(stem)
        candidates.add(stem + "e")
    if token.endswith("ed") and len(token) > 3:
        stem = token[:-2]
        candidates.add(stem)
        candidates.add(stem + "e")
    if token.endswith("es") and len(token) > 3:
        candidates.add(token[:-2])
        candidates.add(token[:-1])
    elif token.endswith("s") and len(token) > 2:
        candidates.add(token[:-1])

    return candidates


def objective_analysis(objective: str) -> dict:
    """Return matched Bloom evidence and the highest matched cognitive level."""
    if not isinstance(objective, str) or not objective.strip():
        raise ValueError("objective must be a non-empty string")

    tokens = _tokens(objective)
    matches = []

    for token in tokens:
        candidates = _candidate_bases(token)
        for level in BLOOM_ORDER:
            matched = sorted(candidates & BLOOM_VERBS[level])
            if matched:
                matches.append(
                    {
                        "token": token,
                        "verb": matched[0],
                        "level": level,
                    }
                )
                break

    matched_levels = [
        match["level"]
        for match in matches
    ]
    level = (
        max(matched_levels, key=BLOOM_ORDER.index)
        if matched_levels
        else None
    )

    return {
        "level": level,
        "matches": matches,
        "matched_levels": sorted(
            set(matched_levels),
            key=BLOOM_ORDER.index,
        ),
    }


def infer_level(objective: str) -> str | None:
    """Infer the highest matched Bloom level, or None when evidence is absent."""
    return objective_analysis(objective)["level"]


def _allocate_minutes(
    total: int,
    shares: tuple[float, ...],
) -> list[int]:
    if isinstance(total, bool) or not isinstance(total, int):
        raise ValueError("minutes must be an integer")
    if total <= 0:
        raise ValueError("minutes must be positive")
    if not shares or any(share < 0 for share in shares):
        raise ValueError("shares must be non-negative and non-empty")
    if not math.isclose(sum(shares), 1.0, abs_tol=1e-9):
        raise ValueError("shares must sum to 1")

    stage_count = len(shares)

    if total >= stage_count:
        allocated = [1] * stage_count
        remaining = total - stage_count
        raw = [remaining * share for share in shares]
    else:
        allocated = [0] * stage_count
        remaining = total
        raw = [remaining * share for share in shares]

    floors = [int(value) for value in raw]
    allocated = [
        base + extra
        for base, extra in zip(allocated, floors)
    ]
    remainder = total - sum(allocated)

    order = sorted(
        range(stage_count),
        key=lambda index: (raw[index] - floors[index], -index),
        reverse=True,
    )
    for index in order[:remainder]:
        allocated[index] += 1

    return allocated


def _accessibility_prompts(
    delivery_mode: str | None,
    accessibility_needs: Iterable[str] | None,
) -> list[str]:
    mode = (
        delivery_mode.strip().lower()
        if isinstance(delivery_mode, str) and delivery_mode.strip()
        else "not specified"
    )
    needs = [
        str(need).strip()
        for need in (accessibility_needs or [])
        if str(need).strip()
    ]

    prompts = [
        "Check whether instructions use clear language and make task expectations explicit.",
        "Offer more than one appropriate way to access important information when the lesson relies on a single representation.",
        "Offer more than one appropriate way to demonstrate learning when that does not change the construct being assessed.",
    ]

    if any(term in mode for term in ("online", "digital", "hybrid", "blended")):
        prompts.extend(
            [
                "Verify keyboard access and visible focus for required digital interactions.",
                "Provide text alternatives for meaningful visuals and captions or transcripts for required audio/video.",
            ]
        )
    elif any(term in mode for term in ("in-person", "classroom", "face-to-face")):
        prompts.append(
            "Check that spoken, visual, and printed directions remain available to learners who need another representation."
        )
    else:
        prompts.append(
            "Specify the delivery mode before treating accessibility planning as complete."
        )

    for need in needs:
        prompts.append(
            f"Review the lesson with the stated learner need in mind: {need}."
        )

    return prompts


def _review_flags(
    *,
    level: str | None,
    matched_levels: list[str],
    minutes: int,
    audience: str | None,
    delivery_mode: str | None,
    prior_knowledge: str | None,
    assessment_mode: str | None,
    accessibility_needs: Iterable[str] | None,
) -> list[str]:
    flags = []

    if level is None:
        flags.append("objective_level_unknown")
    if len(matched_levels) > 1:
        flags.append("multiple_cognitive_levels_detected")
    if minutes < 20:
        flags.append("duration_review")
    if not isinstance(audience, str) or not audience.strip():
        flags.append("audience_not_specified")
    if not isinstance(delivery_mode, str) or not delivery_mode.strip():
        flags.append("delivery_mode_not_specified")
    if not isinstance(prior_knowledge, str) or not prior_knowledge.strip():
        flags.append("prior_knowledge_not_specified")
    if not isinstance(assessment_mode, str) or not assessment_mode.strip():
        flags.append("assessment_mode_not_specified")
    if not list(accessibility_needs or []):
        flags.append("accessibility_needs_not_specified")

    return flags


def lesson_blueprint(
    topic: str,
    objective: str,
    minutes: int = 60,
    *,
    audience: str | None = None,
    delivery_mode: str | None = None,
    prior_knowledge: str | None = None,
    class_size: int | None = None,
    assessment_mode: str | None = None,
    accessibility_needs: Iterable[str] | None = None,
) -> dict:
    """Build an adaptive, deterministic lesson-design scaffold for review."""
    if not isinstance(topic, str) or not topic.strip():
        raise ValueError("topic must be a non-empty string")
    if not isinstance(objective, str) or not objective.strip():
        raise ValueError("objective must be a non-empty string")
    if isinstance(minutes, bool) or not isinstance(minutes, int) or minutes <= 0:
        raise ValueError("minutes must be a positive integer")
    if class_size is not None:
        if (
            isinstance(class_size, bool)
            or not isinstance(class_size, int)
            or class_size <= 0
        ):
            raise ValueError("class_size must be a positive integer when provided")

    analysis = objective_analysis(objective)
    level = analysis["level"]
    template_key = level or "unknown"
    template = LEVEL_TEMPLATES[template_key]
    durations = _allocate_minutes(minutes, template["shares"])

    sequence = []
    for (phase, rationale), duration in zip(template["phases"], durations):
        sequence.append(
            {
                "phase": phase,
                "minutes": duration,
                "rationale": rationale,
            }
        )

    needs = list(accessibility_needs or [])
    review_flags = _review_flags(
        level=level,
        matched_levels=analysis["matched_levels"],
        minutes=minutes,
        audience=audience,
        delivery_mode=delivery_mode,
        prior_knowledge=prior_knowledge,
        assessment_mode=assessment_mode,
        accessibility_needs=needs,
    )

    assessment_prompt = {
        "suggested_evidence": template["assessment"],
        "requested_mode": (
            assessment_mode.strip()
            if isinstance(assessment_mode, str) and assessment_mode.strip()
            else None
        ),
        "alignment_note": (
            "The assessment prompt is selected from the inferred cognitive demand. "
            "A designer must still check subject-matter accuracy, feasibility, and whether "
            "the task actually measures the stated objective."
        ),
    }

    return {
        "topic": topic.strip(),
        "objective": objective.strip(),
        "minutes": minutes,
        "audience": audience.strip() if isinstance(audience, str) and audience.strip() else None,
        "delivery_mode": delivery_mode.strip() if isinstance(delivery_mode, str) and delivery_mode.strip() else None,
        "prior_knowledge": prior_knowledge.strip() if isinstance(prior_knowledge, str) and prior_knowledge.strip() else None,
        "class_size": class_size,
        "assessment_mode": assessment_prompt["requested_mode"],
        "objective_level": level,
        "objective_evidence": analysis["matches"],
        "sequence": sequence,
        "assessment_prompt": assessment_prompt,
        "accessibility_prompts": _accessibility_prompts(delivery_mode, needs),
        "review_flags": review_flags,
        "design_status": "review_required" if review_flags else "ready_for_designer_review",
    }
