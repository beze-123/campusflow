from __future__ import annotations

from campusflow.validation import (
	VALID_CATEGORIES,
	VALID_PRIORITIES,
	VALID_STATUSES,
	VALID_URGENCIES,
	validate_affected_users as _validate_affected_users,
	validate_assignee,
	validate_category,
	validate_status,
	validate_ticket_id,
	validate_title,
	validate_urgency,
)

CATEGORIES = VALID_CATEGORIES
URGENCIES = VALID_URGENCIES
STATUSES = VALID_STATUSES
PRIORITIES = VALID_PRIORITIES


def normalize_category(category: str) -> str:
	return validate_category(category)


def normalize_urgency(urgency: str) -> str:
	return validate_urgency(urgency)


def normalize_status(status: str) -> str:
	return validate_status(status)


def validate_affected_users(affected_users: int) -> int:
	return _validate_affected_users(affected_users)


def calculate_priority(urgency: str, affected_users: int) -> str:
	urgency = normalize_urgency(urgency)
	affected_users = validate_affected_users(affected_users)
	if urgency == "high" and affected_users >= 10:
		return "critical"
	if urgency == "high" or affected_users >= 10:
		return "high"
	if urgency == "medium" or affected_users >= 3:
		return "medium"
	return "low"



def create_ticket(ticket_id: str, title: str, category: str, urgency: str,affected_users: int,) -> dict:
	ticket_id = validate_ticket_id(ticket_id)
	title = validate_title(title)
	urgency = normalize_urgency(urgency)
	affected_users = validate_affected_users(affected_users)
	return {
		"id": ticket_id.strip(),
		"title": title.strip(),
		"category": normalize_category(category),
		"urgency": urgency,
		"affected_users": affected_users,
		"priority": calculate_priority(urgency, affected_users),
		"status": "open",
		"assigned_to": None,
		"notes": [],
	}


def validate_ticket_data(ticket: dict) -> dict:
	base_fields = {
		"id",
		"title",
		"category",
		"urgency",
		"affected_users",
		"priority",
		"status",
		"assigned_to",
	}
	if not isinstance(ticket, dict) or frozenset(ticket) not in {
		frozenset(base_fields),
		frozenset(base_fields | {"notes"}),
	}:
		raise ValueError("Stored ticket has missing or unexpected fields.")

	normalized = create_ticket(
		ticket["id"],
		ticket["title"],
		ticket["category"],
		ticket["urgency"],
		ticket["affected_users"],
	)
	if not isinstance(ticket["priority"], str) or ticket["priority"] != normalized["priority"]:
		raise ValueError(f"Ticket {ticket['id']} has an invalid priority.")
	normalized["status"] = normalize_status(ticket["status"])
	assigned_to = ticket["assigned_to"]

	if assigned_to is None:
		normalized["assigned_to"] = None
	else:
		normalized["assigned_to"] = validate_assignee(assigned_to)

	from campusflow.notes import validate_note_data

	notes = ticket.get("notes", [])
	if not isinstance(notes, list):
		raise ValueError(f"Ticket {ticket['id']} has invalid notes.")
	validated_notes = [validate_note_data(note) for note in notes]
	note_ids = [note["note_id"] for note in validated_notes]
	if len(note_ids) != len(set(note_ids)):
		raise ValueError(f"Ticket {ticket['id']} has duplicate note IDs.")
	normalized["notes"] = validated_notes
	return normalized
