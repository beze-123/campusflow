import unittest

from campusflow.ticket import create_ticket
from campusflow.workflow import (
	assign_ticket,
	get_work_queue,
	reopen_ticket,
	update_ticket_status,
)


def make_ticket(ticket_id, priority="low", status="open", assigned_to=None):
	ticket = create_ticket(ticket_id, ticket_id, "Other", "low", 1)
	ticket["priority"] = priority
	ticket["status"] = status
	ticket["assigned_to"] = assigned_to
	return ticket


class WorkflowTests(unittest.TestCase):
	def test_assigns_ticket_and_normalizes_staff_name(self):
		ticket = make_ticket("T001")

		result = assign_ticket([ticket], "t001", "  Alex Brown  ")

		self.assertIs(result, ticket)
		self.assertEqual(ticket["assigned_to"], "Alex Brown")

	def test_rejects_blank_assignee_without_changing_ticket(self):
		ticket = make_ticket("T001")

		with self.assertRaisesRegex(ValueError, "must not be blank"):
			assign_ticket([ticket], "T001", "   ")

		self.assertIsNone(ticket["assigned_to"])

	def test_rejects_unknown_ticket_id(self):
		with self.assertRaisesRegex(ValueError, "was not found"):
			assign_ticket([], "T999", "Alex")

	def test_unassigned_ticket_cannot_start_work(self):
		ticket = make_ticket("T001")

		with self.assertRaisesRegex(ValueError, "Assign the ticket"):
			update_ticket_status([ticket], "T001", "in_progress")

		self.assertEqual(ticket["status"], "open")

	def test_assigned_ticket_follows_required_lifecycle(self):
		ticket = make_ticket("T001", assigned_to="Alex")

		update_ticket_status([ticket], "T001", "in progress")
		self.assertEqual(ticket["status"], "in_progress")
		update_ticket_status([ticket], "T001", "resolved")
		self.assertEqual(ticket["status"], "resolved")

	def test_rejects_skipped_transition(self):
		ticket = make_ticket("T001", assigned_to="Alex")

		with self.assertRaisesRegex(ValueError, "Cannot move ticket"):
			update_ticket_status([ticket], "T001", "resolved")

		self.assertEqual(ticket["status"], "open")

	def test_resolved_ticket_requires_explicit_reopen(self):
		ticket = make_ticket("T001", status="resolved", assigned_to="Alex")

		with self.assertRaisesRegex(ValueError, "reopen"):
			assign_ticket([ticket], "T001", "Sam")
		with self.assertRaisesRegex(ValueError, "reopen action"):
			update_ticket_status([ticket], "T001", "open")

		reopen_ticket([ticket], "T001")
		self.assertEqual(ticket["status"], "open")
		assign_ticket([ticket], "T001", "Sam")
		self.assertEqual(ticket["assigned_to"], "Sam")

	def test_only_resolved_tickets_can_be_reopened(self):
		ticket = make_ticket("T001")

		with self.assertRaisesRegex(ValueError, "Only resolved"):
			reopen_ticket([ticket], "T001")

		self.assertEqual(ticket["status"], "open")

	def test_work_queue_orders_priority_then_numeric_id_and_excludes_resolved(self):
		tickets = [
			make_ticket("T010", priority="high", status="open"),
			make_ticket("T003", priority="critical", status="in_progress"),
			make_ticket("T002", priority="critical", status="open"),
			make_ticket("T001", priority="critical", status="resolved"),
			make_ticket("T004", priority="low", status="open"),
		]

		queue = get_work_queue(tickets)

		self.assertEqual([ticket["id"] for ticket in queue], [
			"T002", "T003", "T010", "T004"
		])


if __name__ == "__main__":
	unittest.main()
