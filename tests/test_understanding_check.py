import unittest

from campusflow.understanding_check import (
	QUESTIONS,
	run_understanding_check,
	score_answers,
)


class UnderstandingCheckTests(unittest.TestCase):
	def test_score_uses_submitted_answers(self):
		correct_answers = [question["answer"] for question in QUESTIONS]
		self.assertEqual(score_answers(correct_answers), 6)
		self.assertEqual(score_answers(["A"] * 6), 0)
		self.assertEqual(score_answers(["B", "A", "B", "C", "A", "B"]), 4)

	def test_invalid_choice_retries_and_explanations_are_displayed(self):
		answers = iter(["x", "B", "C", "B", "C", "C", "B", "State is unchanged", "Reject duplicates"])
		output = []

		score = run_understanding_check(
			input_func=lambda prompt: next(answers),
			output_func=output.append,
		)

		self.assertEqual(score, 6)
		self.assertTrue(any("Enter A, B, C, or D." in line for line in output))
		self.assertTrue(any("State is unchanged" in line for line in output))
		self.assertTrue(any("Reject duplicates" in line for line in output))

	def test_score_requires_six_answers(self):
		with self.assertRaisesRegex(ValueError, "6 answers"):
			score_answers(["A"])


if __name__ == "__main__":
	unittest.main()
