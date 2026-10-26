# Team Design Decisions

## Ticket and mutation contract

- Tickets are dictionaries with `id`, `title`, `category`, `urgency`, `affected_users`, `priority`, `status`, `assigned_to`, and `notes`.
- `create_ticket` centralizes ticket validation and calculates priority using the required precedence. `validate_ticket_data` accepts legacy records without `notes` and supplies an empty list.
- Workflow and note functions validate their inputs and preconditions before mutating a ticket. Invalid operations raise `ValueError`; the CLI reports the failure without saving the rejected operation.
- The normal lifecycle is `open` → `in_progress` → `resolved`; only resolved tickets can be reopened. An open ticket must be assigned before starting work.
- Resolved tickets cannot be assigned or accept new notes until reopened. Existing notes remain attached through transitions.

## Search, queue, and reporting

- `search_tickets` is read-only. Every supplied category, status, and priority filter must match, alongside the optional case-insensitive title substring.
- The original work queue contains only `open` tickets. It sorts by priority, then the numeric ticket ID. In-progress work is counted as unresolved in reports but is not part of that queue.
- Reports count each ticket once by its current status. Resolution percentage is `resolved / total * 100`, or zero when the collection is empty.

## Persistence

- JSON remains a top-level list of ticket objects. Legacy objects without `notes` remain supported.
- The entire collection is validated, including unique ticket IDs, priority consistency, legal statuses, and unique valid note IDs per ticket, before load results are returned or a save replaces the existing file.
- Saves use a temporary file in the target directory and atomic replacement. Invalid collections are rejected before writing.

## Collaboration evidence still required

The repository can verify code and tests, but not both engineers' identities, individual authorship, independent learning reflections, partner review comments, PR approvals, or mentor review. Add those links and records to the submission after the engineers complete them.
