VALID_CATEGORIES = {
    "network": "Network",
    "hardware": "Hardware",
    "software": "Software",
    "other": "Other",
}

VALID_URGENCIES = {"low", "medium", "high"}

VALID_STATUSES = {"open", "in_progress", "resolved"}


def validate_title(title):
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Title cannot be blank.")

    return title.strip()


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


def validate_affected_users(affected_users):
    if isinstance(affected_users, bool):
        raise ValueError("affected_users must be a positive integer.")

    if not isinstance(affected_users, int):
        raise ValueError("affected_users must be a positive integer.")

    if affected_users <= 0:
        raise ValueError("affected_users must be a positive integer.")

    return affected_users