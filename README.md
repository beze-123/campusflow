# CampusFlow

CampusFlow is a Python command-line ticket manager for campus technical support. It uses only the Python standard library and stores tickets in a JSON file.

## Requirements

- Python 3.10 or later
- No third-party packages

## Run

```bash
python main.py
```

The app reads and writes `tickets.json` in the current working directory. Choose a menu option to create, list, inspect, assign, transition, reopen, search, report on, or add/view notes for tickets. The menu also includes the Engineering Understanding Check.

Run the full automated suite with:

```bash
python -m unittest discover -s tests -v
```

## Ticket Rules

Tickets have `id`, `title`, `category`, `urgency`, `affected_users`, `priority`, `status`, `assigned_to`, and `notes`. IDs use `T001`, `T002`, and subsequent numeric values. New tickets start open and unassigned, with an empty notes list.

Categories are Network, Hardware, Software, and Other. Urgency is low, medium, or high. Titles must not be blank, and affected users must be a positive integer (booleans, floats, and strings are rejected).

Priority follows this ordered rule:

1. High urgency and at least 10 affected users: `critical`.
2. High urgency or at least 10 affected users: `high`.
3. Medium urgency or at least 3 affected users: `medium`.
4. Otherwise: `low`.

The normal lifecycle is `open` → `in_progress` → `resolved`; an unassigned ticket cannot enter `in_progress`. Resolved tickets must be reopened before assignment changes or new notes. Existing notes remain after resolve/reopen.

## Search, Queue, and Reports

Search matches a case-insensitive title substring and optional category, status, and priority filters. Supplied filters are combined with AND. Search results can be shown separately in priority order (critical, high, medium, low), then numeric ticket ID order.

The original Open Work Queue contains **only open tickets**, ordered by priority and numeric ticket ID. It does not include in-progress tickets.

Reports include total tickets, status and priority counts, category counts, unresolved and resolved totals, and resolution percentage. Unresolved means open plus in-progress; resolution percentage is zero when there are no tickets. Counts use each ticket's current status.

## JSON Format and Compatibility

The data file is a JSON list of ticket objects. Each object contains the ticket fields above. `notes` is a list of objects with `note_id`, `author`, and `message`; note IDs are per-ticket (`N001`, `N002`, ...).

For compatibility, older list-format ticket objects without `notes` load with an empty notes list. Loading validates the entire collection, including IDs, priority consistency, legal statuses, and note shapes, before returning records. Invalid JSON or records are rejected; saving validates before atomically replacing the file. Existing ticket records and notes are not discarded.

## Learning and Delivery Evidence

See [docs/baseline-check.md](docs/baseline-check.md), [docs/design-decisions.md](docs/design-decisions.md), and [docs/ai-learning-log.md](docs/ai-learning-log.md). Baseline details and individual learning, partner-review, and submission evidence must be completed by the engineers; the repository alone cannot establish personal authorship or review approval.
