import unittest

from campusflow.notes import add_note, get_ticket_notes, next_note_id
from campusflow.ticket import create_ticket
from campusflow.workflow import assign_ticket, reopen_ticket, update_ticket_status


class NoteTests(unittest.TestCase):
	def make_ticket(self):
		return create_ticket("T001", "Wi-Fi issue", "Network", "high", 1)

	def test_add_note_trims_fields_and_assigns_first_id(self):
		ticket = self.make_ticket()

		note = add_note([ticket], "T001", "  Mentor A ", "  Router reboot tried  ")

		self.assertEqual(
			note,
			{
				"note_id": "N001",
				"author": "Mentor A",
				"message": "Router reboot tried",
			},
		)
		self.assertEqual(get_ticket_notes([ticket], "T001"), [note])

	def test_rejected_note_does_not_change_ticket_or_consume_id(self):
		ticket = self.make_ticket()
		original = {key: value.copy() if isinstance(value, list) else value for key, value in ticket.items()}

		for author, message in ((" ", "Valid message"), ("Mentor", "Nope")):
			with self.subTest(author=author, message=message):
				with self.assertRaises(ValueError):
					add_note([ticket], "T001", author, message)
				self.assertEqual(ticket, original)

		self.assertEqual(add_note([ticket], "T001", "Mentor", "Valid message")["note_id"], "N001")

	def test_resolved_ticket_rejects_notes_until_reopened(self):
		ticket = self.make_ticket()
		tickets = [ticket]
		add_note(tickets, "T001", "Mentor A", "Initial update")
		assign_ticket(tickets, "T001", "Alex")
		update_ticket_status(tickets, "T001", "in_progress")
		update_ticket_status(tickets, "T001", "resolved")

		with self.assertRaisesRegex(ValueError, "reopened"):
			add_note(tickets, "T001", "Mentor B", "Follow-up update")
		self.assertEqual([note["note_id"] for note in ticket["notes"]], ["N001"])

		reopen_ticket(tickets, "T001")
		second_note = add_note(tickets, "T001", "Mentor B", "Follow-up update")
		self.assertEqual(second_note["note_id"], "N002")
		self.assertEqual(
			[note["note_id"] for note in get_ticket_notes(tickets, "T001")],
			["N001", "N002"],
		)

	def test_next_note_id_uses_highest_existing_number(self):
		ticket = self.make_ticket()
		ticket["notes"] = [
			{"note_id": "N003", "author": "A", "message": "Valid note"},
			{"note_id": "N001", "author": "B", "message": "Valid note"},
		]

		self.assertEqual(next_note_id(ticket), "N004")


if __name__ == "__main__":
	unittest.main()
