def search_tickets(
    tickets,
    title="",
    category=None,
    status=None,
    priority=None
):
    results = []

    for ticket in tickets:

        # Title filter
        if title and title.casefold() not in ticket["title"].casefold():
            continue

        # Category filter
        if category and ticket["category"] != category:
            continue

        # Status filter
        if status and ticket["status"] != status:
            continue

        # Priority filter
        if priority and ticket["priority"] != priority:
            continue

        results.append(ticket)

    return results