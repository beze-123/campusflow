from __future__ import annotations


CATEGORIES = {
	"network": "Network",
	"hardware": "Hardware",
	"software": "Software",
	"other": "Other",
}
URGENCIES = {"low", "medium", "high"}
STATUSES = {"open", "in_progress", "resolved"}
PRIORITIES = {"low", "medium", "high", "critical"}


def normalize_category(category: str) -> str:
	if not isinstance(category, str):
		raise ValueError("Category must be Network, Hardware, Software, or Other.")
	normalized = CATEGORIES.get(category.strip().casefold())
	if normalized is None:
		raise ValueError("Category must be Network, Hardware, Software, or Other.")
	return normalized


def normalize_urgency(urgency: str) -> str:
	if not isinstance(urgency, str):
		raise ValueError("Urgency must be low, medium, or high.")
	normalized = urgency.strip().casefold()
	if normalized not in URGENCIES:
		raise ValueError("Urgency must be low, medium, or high.")
	return normalized


def normalize_status(status: str) -> str:
	if not isinstance(status, str):
		raise ValueError("Status must be open, in_progress, or resolved.")
	normalized = status.strip().casefold().replace(" ", "_").replace("-", "_")
	if normalized not in STATUSES:
		raise ValueError("Status must be open, in_progress, or resolved.")
	return normalized


def validate_affected_users(affected_users: int) -> int:
	if isinstance(affected_users, bool) or not isinstance(affected_users, int):
		raise ValueError("Affected users must be a positive integer.")
	if affected_users <= 0:
		raise ValueError("Affected users must be a positive integer.")
	return affected_users


def calculate_priority(urgency: str, affected_users: int) -> str:
	urgency = normalize_urgency(urgency)
	affected_users = validate_affected_users(affected_users)
	if urgency == "high":
		return "critical" if affected_users >= 10 else "high"
	if urgency == "medium":
		return "high" if affected_users >= 10 else "medium"
	return "medium" if affected_users >= 10 else "low"



def create_ticket(ticket_id: str, title: str, category: str, urgency: str,affected_users: int,) -> dict:
	if not isinstance(ticket_id, str) or not ticket_id.strip():
		raise ValueError("Ticket ID must not be blank.")
	if not isinstance(title, str) or not title.strip():
		raise ValueError("Title must not be blank.")


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
	}


def validate_ticket_data(ticket: dict) -> dict:
	required_fields = {
		"id",
		"title",
		"category",
		"urgency",
		"affected_users",
		"priority",
		"status",
		"assigned_to",
	}
	if not isinstance(ticket, dict) or set(ticket) != required_fields:
		raise ValueError("Stored ticket has missing or unexpected fields.")

	normalized = create_ticket(
		ticket["id"],
		ticket["title"],
		ticket["category"],
		ticket["urgency"],
		ticket["affected_users"],
	)
	if ticket["priority"] != normalized["priority"]:
		raise ValueError(f"Ticket {ticket['id']} has an invalid priority.")
	
	normalized["status"] = normalize_status(ticket["status"])
	assigned_to = ticket["assigned_to"]

	if assigned_to is not None and (
		not isinstance(assigned_to, str) or not assigned_to.strip()
	):
		raise ValueError(f"Ticket {ticket['id']} has an invalid assignee.")
	normalized["assigned_to"] = assigned_to.strip() if assigned_to else None
	return normalized
