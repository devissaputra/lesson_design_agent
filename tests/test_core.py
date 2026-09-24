import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from lesson_design_agent import core


class CoreTests(unittest.TestCase):
    def test_infer_level_returns_highest_matched_level(self):
        self.assertEqual(
            core.infer_level("Compare two options and design a solution."),
            "create",
        )

    def test_infer_level_returns_none_when_no_verb_matches(self):
        self.assertIsNone(core.infer_level("Operational risk awareness"))

    def test_infer_level_handles_inflected_verbs(self):
        self.assertEqual(
            core.infer_level("Learners will be analyzing operational risks."),
            "analyze",
        )

    def test_infer_level_recognizes_compare(self):
        self.assertEqual(
            core.infer_level("Compare two risk controls."),
            "analyze",
        )

    def test_infer_level_recognizes_evaluate(self):
        self.assertEqual(
            core.infer_level("Evaluate the response plan."),
            "evaluate",
        )

    def test_objective_analysis_preserves_evidence(self):
        result = core.objective_analysis("Analyze evidence and justify a recommendation.")
        self.assertEqual(result["level"], "evaluate")
        self.assertIn("analyze", result["matched_levels"])
        self.assertIn("evaluate", result["matched_levels"])
        self.assertGreaterEqual(len(result["matches"]), 2)

    def test_objective_analysis_rejects_empty_input(self):
        with self.assertRaises(ValueError):
            core.objective_analysis(" ")

    def test_time_budget_is_exact(self):
        plan = core.lesson_blueprint(
            "Risk analysis",
            "Analyze operational risk.",
            90,
        )
        self.assertEqual(
            sum(stage["minutes"] for stage in plan["sequence"]),
            90,
        )

    def test_time_budget_is_exact_for_awkward_lengths(self):
        for minutes in (1, 6, 29, 61):
            plan = core.lesson_blueprint(
                "Risk analysis",
                "Explain operational risk.",
                minutes,
            )
            self.assertEqual(
                sum(stage["minutes"] for stage in plan["sequence"]),
                minutes,
            )

    def test_four_phases_receive_minutes_when_duration_allows(self):
        plan = core.lesson_blueprint(
            "Risk analysis",
            "Apply the risk matrix.",
            20,
        )
        self.assertTrue(
            all(stage["minutes"] >= 1 for stage in plan["sequence"])
        )

    def test_apply_sequence_differs_from_create_sequence(self):
        apply_plan = core.lesson_blueprint(
            "Risk analysis",
            "Apply the risk matrix.",
            60,
        )
        create_plan = core.lesson_blueprint(
            "Risk analysis",
            "Design a risk treatment plan.",
            60,
        )
        self.assertNotEqual(
            [stage["phase"] for stage in apply_plan["sequence"]],
            [stage["phase"] for stage in create_plan["sequence"]],
        )

    def test_analyze_sequence_contains_guided_analysis(self):
        plan = core.lesson_blueprint(
            "Risk analysis",
            "Analyze operational risk.",
            60,
        )
        self.assertIn(
            "guided analysis",
            [stage["phase"] for stage in plan["sequence"]],
        )

    def test_create_sequence_emphasizes_iterative_construction(self):
        plan = core.lesson_blueprint(
            "Prototype design",
            "Design and revise a prototype.",
            60,
        )
        stage_names = [stage["phase"] for stage in plan["sequence"]]
        self.assertIn("iterative construction", stage_names)

    def test_unknown_objective_sets_review_flag(self):
        plan = core.lesson_blueprint(
            "Risk analysis",
            "Operational risk awareness",
            60,
        )
        self.assertIsNone(plan["objective_level"])
        self.assertIn("objective_level_unknown", plan["review_flags"])

    def test_multiple_levels_set_review_flag(self):
        plan = core.lesson_blueprint(
            "Risk analysis",
            "Explain the framework and evaluate a response plan.",
            60,
        )
        self.assertIn(
            "multiple_cognitive_levels_detected",
            plan["review_flags"],
        )

    def test_short_duration_sets_review_flag(self):
        plan = core.lesson_blueprint("x", "Explain x", 10)
        self.assertIn("duration_review", plan["review_flags"])

    def test_missing_context_is_flagged(self):
        plan = core.lesson_blueprint("x", "Explain x", 60)
        self.assertIn("audience_not_specified", plan["review_flags"])
        self.assertIn("delivery_mode_not_specified", plan["review_flags"])
        self.assertIn("prior_knowledge_not_specified", plan["review_flags"])
        self.assertIn("assessment_mode_not_specified", plan["review_flags"])
        self.assertIn(
            "accessibility_needs_not_specified",
            plan["review_flags"],
        )

    def test_complete_context_removes_context_flags(self):
        plan = core.lesson_blueprint(
            "Risk analysis",
            "Analyze operational risk.",
            90,
            audience="early-career operations analysts",
            delivery_mode="hybrid",
            prior_knowledge="basic probability and process mapping",
            class_size=24,
            assessment_mode="case analysis",
            accessibility_needs=["captions for video"],
        )
        self.assertNotIn("audience_not_specified", plan["review_flags"])
        self.assertNotIn("delivery_mode_not_specified", plan["review_flags"])
        self.assertNotIn("prior_knowledge_not_specified", plan["review_flags"])
        self.assertNotIn("assessment_mode_not_specified", plan["review_flags"])
        self.assertNotIn(
            "accessibility_needs_not_specified",
            plan["review_flags"],
        )

    def test_online_mode_adds_digital_accessibility_prompts(self):
        plan = core.lesson_blueprint(
            "Risk analysis",
            "Analyze operational risk.",
            60,
            delivery_mode="online",
        )
        joined = " ".join(plan["accessibility_prompts"]).lower()
        self.assertIn("keyboard", joined)
        self.assertIn("captions", joined)

    def test_unspecified_mode_requests_mode_before_completion(self):
        plan = core.lesson_blueprint(
            "Risk analysis",
            "Analyze operational risk.",
            60,
        )
        self.assertTrue(
            any(
                "specify the delivery mode" in prompt.lower()
                for prompt in plan["accessibility_prompts"]
            )
        )

    def test_accessibility_need_is_carried_into_prompt(self):
        plan = core.lesson_blueprint(
            "Risk analysis",
            "Analyze operational risk.",
            60,
            accessibility_needs=["screen reader compatibility"],
        )
        joined = " ".join(plan["accessibility_prompts"]).lower()
        self.assertIn("screen reader compatibility", joined)

    def test_assessment_prompt_changes_by_level(self):
        apply_plan = core.lesson_blueprint(
            "Risk analysis",
            "Apply the risk matrix.",
            60,
        )
        evaluate_plan = core.lesson_blueprint(
            "Risk analysis",
            "Evaluate the response plan.",
            60,
        )
        self.assertNotEqual(
            apply_plan["assessment_prompt"]["suggested_evidence"],
            evaluate_plan["assessment_prompt"]["suggested_evidence"],
        )

    def test_topic_must_be_string(self):
        with self.assertRaises(ValueError):
            core.lesson_blueprint(None, "Explain x", 60)

    def test_objective_must_be_string(self):
        with self.assertRaises(ValueError):
            core.lesson_blueprint("x", None, 60)

    def test_minutes_reject_boolean(self):
        with self.assertRaises(ValueError):
            core.lesson_blueprint("x", "Explain x", True)

    def test_minutes_reject_float(self):
        with self.assertRaises(ValueError):
            core.lesson_blueprint("x", "Explain x", 60.5)

    def test_class_size_validation(self):
        with self.assertRaises(ValueError):
            core.lesson_blueprint(
                "x",
                "Explain x",
                60,
                class_size=0,
            )

    def test_output_sequence_contains_rationale(self):
        plan = core.lesson_blueprint(
            "Risk analysis",
            "Analyze operational risk.",
            60,
        )
        self.assertTrue(
            all(stage["rationale"] for stage in plan["sequence"])
        )


if __name__ == "__main__":
    unittest.main()
