import re

from campusflow.validation import validate_assignee, validate_ticket_id


def validate_note_message(message):
	if not isinstance(message, str):
		raise ValueError("Note message must be 5 to 300 characters.")

	normalized = message.strip()
	if not 5 <= len(normalized) <= 300:
		raise ValueError("Note message must be 5 to 300 characters.")

	return normalized


def validate_note_data(note):
	if not isinstance(note, dict) or set(note) != {"note_id", "author", "message"}:
		raise ValueError("Stored note has missing or unexpected fields.")

	note_id = note["note_id"]
	if not isinstance(note_id, str) or not re.fullmatch(r"N\d{3,}", note_id):
		raise ValueError("Note ID must use the N<number> format.")

	return {
		"note_id": note_id,
		"author": validate_assignee(note["author"]),
		"message": validate_note_message(note["message"]),
	}


def next_note_id(ticket):
	numbers = [int(note["note_id"][1:]) for note in ticket.get("notes", [])]
	return f"N{max(numbers, default=0) + 1:03d}"


def _find_ticket(tickets, ticket_id):
	normalized_id = validate_ticket_id(ticket_id)
	for ticket in tickets:
		if ticket["id"] == normalized_id:
			return ticket

	raise ValueError(f"Ticket {ticket_id} was not found.")


def add_note(tickets, ticket_id, author, message):
	normalized_id = validate_ticket_id(ticket_id)
	normalized_author = validate_assignee(author)
	normalized_message = validate_note_message(message)
	ticket = _find_ticket(tickets, normalized_id)
	if ticket["status"] not in {"open", "in_progress"}:
		raise ValueError("Resolved tickets must be reopened before adding notes.")

	note = {
		"note_id": next_note_id(ticket),
		"author": normalized_author,
		"message": normalized_message,
	}
	ticket["notes"].append(note)
	return note


def get_ticket_notes(tickets, ticket_id):
	ticket = _find_ticket(tickets, ticket_id)
	return sorted(ticket["notes"], key=lambda note: int(note["note_id"][1:]))
