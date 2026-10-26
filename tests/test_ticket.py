import unittest

from campusflow.ticket import calculate_priority, create_ticket


class TicketTests(unittest.TestCase):
	def test_create_ticket_normalizes_inputs_and_calculates_priority(self):
		ticket = create_ticket(" T001 ", "  Wi-Fi outage  ", "nEtWoRk", "HIGH", 15)

		self.assertEqual(
			ticket,
			{
				"id": "T001",
				"title": "Wi-Fi outage",
				"category": "Network",
				"urgency": "high",
				"affected_users": 15,
				"priority": "critical",
				"status": "open",
				"assigned_to": None,
				"notes": [],
			},
		)

	def test_priority_uses_urgency_and_impact(self):
		self.assertEqual(calculate_priority("high", 1), "high")
		self.assertEqual(calculate_priority("high", 10), "critical")
		self.assertEqual(calculate_priority("medium", 10), "high")
		self.assertEqual(calculate_priority("low", 3), "medium")
		self.assertEqual(calculate_priority("low", 9), "medium")
		self.assertEqual(calculate_priority("low", 10), "high")

	def test_rejects_invalid_ticket_inputs(self):
		invalid_inputs = [0, -1, 1.5, "5", True]
		for affected_users in invalid_inputs:
			with self.subTest(affected_users=affected_users):
				with self.assertRaisesRegex(ValueError, "positive integer"):
					create_ticket("T001", "Issue", "Other", "low", affected_users)

		for title, category, urgency in (
			("   ", "Other", "low"),
			("Issue", "Printer", "low"),
			("Issue", "Other", "urgent"),
		):
			with self.subTest(title=title, category=category, urgency=urgency):
				with self.assertRaises(ValueError):
					create_ticket("T001", title, category, urgency, 1)

		with self.assertRaisesRegex(ValueError, "T<number>"):
			create_ticket("ticket-1", "Issue", "Other", "low", 1)


if __name__ == "__main__":
	unittest.main()
