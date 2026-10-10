# campusflow

CampusFlow is a Python command-line tool for recording and reviewing campus
technical support tickets. Ticket data is stored in a JSON file so it remains
available after the program exits.

## Requirements

- Python 3.10 or later
- No third-party packages are required

## Run Interactively

Start the menu with:

```bash
python main.py
```

Choose an option from the menu:

1. Create a ticket. Enter a title, category, urgency, and number of affected
	users. Invalid values produce an error and are prompted again.
2. Show all saved tickets in a table.
3. View one ticket's details by entering its ID, such as `T001`.
4. Quit.

The menu continues until you choose **Quit**. To use a different data file,
pass its path when starting the program:

```bash
python main.py --data data/campus-tickets.json
```

By default, data is saved to `tickets.json` in the current directory.

## Command-Line Shortcuts

Tickets can also be created or listed without opening the menu:

```bash
python main.py add --title "Campus Wi-Fi is down" --category Network --urgency high --affected-users 15
python main.py list
```

Use `--data PATH` before the command to select a different JSON file:

```bash
python main.py --data data/campus-tickets.json list
```

## Ticket Rules

Each ticket contains `id`, `title`, `category`, `urgency`, `affected_users`,
`priority`, `status`, and `assigned_to`. IDs are automatically generated in
sequence (`T001`, `T002`, ...). New tickets start with status `open` and no
assignee.

Categories are Network, Hardware, Software, and Other. Urgency is low, medium,
or high. These values are case-insensitive and stored in a consistent form.
Titles must not be blank. Affected users must be a positive whole number.

Priority is calculated from urgency and impact. Ten or more affected users is
treated as high impact:

| Urgency | Fewer than 10 users | 10 or more users |
| --- | --- | --- |
| High | high | critical |
| Medium | medium | high |
| Low | low | medium |

## Current Scope

The current menu supports creating tickets, listing all tickets, and viewing a
ticket's details. Assignment, status updates, and summary reports are not yet
available. The corresponding ticket fields are present; new tickets are
unassigned and open by default.

## Tests

Run the test suite with Python's built-in `unittest` module:

```bash
python -m unittest discover -s tests -v
```