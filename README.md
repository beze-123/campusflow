# campusflow

CampusFlow is a Python command-line tool for recording and reviewing campus
technical support tickets. Ticket data is stored in a JSON file so it remains
available after the program exits.

## Requirements

- Python 3.10 or later
- No third-party packages are required

## Run the App

Run the program without command-line arguments to open the interactive menu:

```bash
python main.py
```

Choose an option from the menu:

1. Create a ticket. Enter a title, category, urgency, and number of affected
	users. Invalid values produce an error and are prompted again.
2. Show all saved tickets in a table.
3. View one ticket's details by entering its ID, such as `T001`.
4. Quit.

The menu continues until you choose **Quit**. Ticket data is saved in
`tickets.json` in the current working directory. All ticket actions are done
through the menu; no command-line subcommands or data-file arguments are used.

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