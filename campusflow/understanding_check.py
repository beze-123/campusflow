QUESTIONS = (
	{
		"question": "T001 is open and unassigned. A user tries to move it to in_progress.",
		"options": {
			"A": "Accept",
			"B": "Reject and preserve all data",
			"C": "Resolve it automatically",
			"D": "Remove the ticket",
		},
		"answer": "B",
	},
	{
		"question": "The app has zero tickets. What should resolution percentage display?",
		"options": {
			"A": "Crash",
			"B": "100%",
			"C": "0%",
			"D": "Divide by one without explanation",
		},
		"answer": "C",
	},
	{
		"question": "Search uses title='wifi', category='Network', status='open'. What matches?",
		"options": {
			"A": "Any record matching one filter",
			"B": "Only records matching all supplied filters",
			"C": "All network records",
			"D": "All open records",
		},
		"answer": "B",
	},
	{
		"question": "A resolved ticket receives Add Note. What should happen?",
		"options": {
			"A": "Append anyway",
			"B": "Delete old notes",
			"C": "Reject until reopened",
			"D": "Change status silently",
		},
		"answer": "C",
	},
	{
		"question": "JSON includes two tickets with the same ID. What should load do?",
		"options": {
			"A": "Keep both",
			"B": "Replace memory with duplicates",
			"C": "Reject load without changing current memory",
			"D": "Rename IDs silently",
		},
		"answer": "C",
	},
	{
		"question": "A PR changes validation but has no negative-case tests. What is the best review action?",
		"options": {
			"A": "Approve because it runs",
			"B": "Request focused tests and reasoning",
			"C": "Merge immediately",
			"D": "Ask AI to approve it",
		},
		"answer": "B",
	},
)


def score_answers(answers):
	if len(answers) != len(QUESTIONS):
		raise ValueError(f"Expected {len(QUESTIONS)} answers.")

	return sum(
		isinstance(answer, str) and answer.strip().upper() == question["answer"]
		for question, answer in zip(QUESTIONS, answers)
	)


def run_understanding_check(input_func=None, output_func=None):
	if input_func is None:
		input_func = input
	if output_func is None:
		output_func = print

	answers = []
	for index, question in enumerate(QUESTIONS, start=1):
		output_func(f"\nQ{index}. {question['question']}")
		for letter, option in question["options"].items():
			output_func(f"  {letter}. {option}")

		while True:
			answer = input_func("Answer (A/B/C/D): ").strip().upper()
			if answer in question["options"]:
				answers.append(answer)
				break
			output_func("Enter A, B, C, or D.")

	explanations = []
	for index in (0, 4):
		question_number = index + 1
		explanations.append(
			(
				question_number,
				input_func(f"Briefly explain your answer to Q{question_number}: ").strip(),
			)
		)

	score = score_answers(answers)
	output_func(f"Score: {score}/{len(QUESTIONS)}")
	output_func("Explanations for mentor discussion:")
	for question_number, explanation in explanations:
		output_func(f"Q{question_number}: {explanation or '(no explanation provided)'}")

	return score
