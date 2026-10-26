import re


VALID_CATEGORIES = {
    "network": "Network",
    "hardware": "Hardware",
    "software": "Software",
    "other": "Other",
}

VALID_URGENCIES = {"low", "medium", "high"}

VALID_STATUSES = {"open", "in_progress", "resolved"}
VALID_PRIORITIES = {"critical", "high", "medium", "low"}


def validate_title(title):
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Title cannot be blank.")

    return title.strip()


def validate_ticket_id(ticket_id):
    if not isinstance(ticket_id, str):
        raise ValueError("Ticket ID must use the T<number> format.")

    normalized = ticket_id.strip().upper()
    if not re.fullmatch(r"T\d{3,}", normalized):
        raise ValueError("Ticket ID must use the T<number> format.")

    return normalized


def validate_category(category):
    if not isinstance(category, str):
        raise ValueError("Category must be text.")

    normalized = category.strip().casefold()

    if normalized not in VALID_CATEGORIES:
        raise ValueError("Invalid category.")

    return VALID_CATEGORIES[normalized]


def validate_urgency(urgency):
    if not isinstance(urgency, str):
        raise ValueError("Urgency must be text.")

    normalized = urgency.strip().casefold()

    if normalized not in VALID_URGENCIES:
        raise ValueError("Invalid urgency.")

    return normalized


def validate_status(status):
    if not isinstance(status, str):
        raise ValueError("Status must be open, in_progress, or resolved.")

    normalized = status.strip().casefold().replace(" ", "_").replace("-", "_")
    if normalized not in VALID_STATUSES:
        raise ValueError("Status must be open, in_progress, or resolved.")

    return normalized


def validate_assignee(assignee):
    if not isinstance(assignee, str) or not assignee.strip():
        raise ValueError("Assignee name must not be blank.")

    return assignee.strip()


def validate_affected_users(affected_users):
    if isinstance(affected_users, bool):
        raise ValueError("affected_users must be a positive integer.")

    if not isinstance(affected_users, int):
        raise ValueError("affected_users must be a positive integer.")

    if affected_users <= 0:
        raise ValueError("affected_users must be a positive integer.")

    return affected_users