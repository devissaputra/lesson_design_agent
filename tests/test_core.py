import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from lesson_design_agent import core


class CoreTests(unittest.TestCase):
    def test_blueprint_level_and_time_budget(self):
        plan = core.lesson_blueprint("x", "Design, test, and revise a solution.", 90)
        self.assertEqual(plan["level"], "create")
        self.assertEqual(sum(minutes for _, minutes in plan["sequence"]), 90)

    def test_time_budget_holds_for_awkward_lengths(self):
        for minutes in (1, 6, 29, 61):
            plan = core.lesson_blueprint("x", "Explain x", minutes)
            self.assertEqual(sum(value for _, value in plan["sequence"]), minutes)


if __name__ == "__main__":
    unittest.main()
