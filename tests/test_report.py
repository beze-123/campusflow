import unittest

from campusflow.report import build_report, format_report
from campusflow.ticket import create_ticket


def make_ticket(ticket_id, urgency, affected_users, status, priority=None):
	ticket = create_ticket(ticket_id, ticket_id, "Other", urgency, affected_users)
	ticket["status"] = status
	if priority is not None:
		ticket["priority"] = priority
	return ticket


class ReportTests(unittest.TestCase):
	def test_empty_report_includes_zero_counts_for_each_group(self):
		report = build_report([])

		self.assertEqual(report["total"], 0)
		self.assertEqual(
			report["by_status"],
			{"open": 0, "in_progress": 0, "resolved": 0},
		)
		self.assertEqual(
			report["by_priority"],
			{"critical": 0, "high": 0, "medium": 0, "low": 0},
		)
		self.assertIn("Total tickets: 0", format_report([]))

	def test_report_counts_ticket_statuses_and_priorities(self):
		tickets = [
			make_ticket("T001", "high", 12, "open"),
			make_ticket("T002", "high", 2, "in_progress"),
			make_ticket("T003", "low", 4, "resolved", priority="medium"),
		]

		report = build_report(tickets)

		self.assertEqual(report["total"], 3)
		self.assertEqual(
			report["by_status"],
			{"open": 1, "in_progress": 1, "resolved": 1},
		)
		self.assertEqual(
			report["by_priority"],
			{"critical": 1, "high": 1, "medium": 1, "low": 0},
		)


if __name__ == "__main__":
	unittest.main()
