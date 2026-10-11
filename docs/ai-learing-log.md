# AI Learning Log — CampusFlow

## Task: Ticket Validation and Storage

* **Project:** CampusFlow
* **Language:** Python
* **Feature:** Ticket validation, priority calculation, and JSON storage

---

## What I Worked On

I worked on the **ticket validation and storage system** for CampusFlow.

The main responsibilities were:

* Validating and normalizing ticket information.
* Calculating ticket priority.
* Loading tickets from a JSON file.
* Saving tickets safely to a JSON file.
* Detecting invalid or duplicate stored tickets.

---

## What I Learned

### Ticket Validation

I learned how to create small validation functions with clear responsibilities.

* `normalize_category()` validates and formats categories.
* `normalize_urgency()` validates urgency levels.
* `normalize_status()` validates ticket statuses.
* `validate_affected_users()` ensures affected users is a positive integer.

I also learned that `casefold()` helps normalize text regardless of capitalization.

For example, `"HIGH"` can safely become `"high"`.

### Priority Calculation

I used `calculate_priority()` to calculate priority from **urgency and impact**.

* High urgency + 10 or more affected users → `critical`
* High urgency or 10+ affected users → `high`
* Medium urgency or 3+ affected users → `medium`
* Otherwise → `low`

This helped me understand how business requirements become Python conditional logic.

---

## JSON Storage

I created the `TicketStorage` class for persistent ticket storage.

### `load()`

The method:

* Returns an empty list when the file does not exist.
* Reads ticket data using `json.load()`.
* Ensures the JSON contains a list.
* Validates every stored ticket.
* Detects duplicate ticket IDs.

### `save()`

The method:

* Creates directories when necessary.
* Writes tickets to a temporary file.
* Uses `json.dump()` to create formatted JSON.
* Uses `os.replace()` to safely replace the original file.
* Cleans up temporary files after the operation.

---

## Error Handling

I created a custom `StorageError` for storage-related failures.

I learned how `try`, `except`, and `finally` work together and how:

`raise StorageError(...) from error`

preserves the original error while providing a clearer application-level message.

---

## How AI Helped Me

I used AI as a **learning and code-review assistant**.

AI helped me understand:

* JSON file handling.
* Input normalization and validation.
* Custom exceptions and exception chaining.
* Safe file writing with temporary files.
* Duplicate ID detection.
* Why Boolean values need special handling when validating integers.

I reviewed and understood the suggestions before applying them.

---

## How I Verified the Work

I checked both valid and invalid scenarios.

* Valid tickets are normalized correctly.
* Priorities follow the required business rules.
* Invalid categories, urgency, and statuses are rejected.
* `affected_users` must be a positive integer.
* Invalid stored tickets and duplicate IDs are rejected.
* Valid tickets can be saved and loaded successfully.

---

## Key Takeaway

I learned that persistent storage is more than simply reading and writing JSON.

A reliable system must **validate data, enforce business rules, handle errors, prevent corrupted writes, and verify stored information**.

AI supported my learning, while I remained responsible for understanding and verifying the final implementation.



## ENGINEER B 

# AI Learning Log — CampusFlow

## Task: Workflow and Ticket Assignment Logic

- **Project:** CampusFlow
- **Language:** Python
- **Feature:** Input validation, ticket assignment, and error handling

---

## What I Worked On

I worked on the **workflow and ticket assignment module** (`campusflow/workflow.py`) for CampusFlow.

The main responsibilities were:

- Validating and cleaning staff assignment inputs.
- Searching ticket collections for specific ticket IDs.
- Updating ticket metadata in-place upon finding matches.
- Ensuring robust exception handling for missing items and bad inputs.
- Navigating git pull request, review, and merge workflows on GitHub.

---

## What I Learned

### Input Guard Clauses & String Normalization

I learned how to enforce strict data contracts on input parameters before processing workflow operations.

- Used `isinstance(assigned_to, str)` to ensure the input is explicitly a string.
- Used `.strip() == ""` to catch empty or whitespace-only staff names.
- Leveraged `.strip()` to cleanly sanitize user strings before saving them to the ticket dict.

For example, `"  Alice  "` safely becomes `"Alice"`, while whitespace-only inputs like `"   "` raise a `ValueError`.

### Exception Scope & Loop Control

I learned how the structural placement of `raise` statements affects loop execution.

- Keeping `return ticket` inside the loop terminates execution as soon as a matching ID is found.
- Moving `raise KeyError(...)` outside the `for` loop ensures every ticket in the collection is checked before declaring an ID missing.
- Unindenting the exception handler prevents the function from crashing prematurely on the very first mismatched ticket.

---

## Error Handling & Logic Design

### Explicit `raise` vs. Silent `return`

I evaluated whether to return default values (like `None`) or raise exceptions when operations fail.

- **`return None`**: Silent error codes can pass downstream silently, causing obscure `TypeError` crashes later in the execution flow.
- **`raise Exception`**: Explicitly raising `ValueError` (for bad input) and `KeyError` (for missing tickets) halts execution immediately, enforcing clean interface contracts and allowing callers to use `try...except` cleanly.

---

## How AI Helped Me

I used AI as a **collaborative partner and code-review assistant**.

AI helped me understand:

- The necessity of raising standard Python exceptions over returning `None`.
- How indentation directly controls loop iteration and exception boundaries.
- Resolving GitHub Pull Request workflows (understanding self-approval limitations vs. comment reviews).
- Extracting exact Git commit SHAs using terminal commands (`git rev-parse HEAD`).

I authored the implementation line-by-line and verified all logic choices before merging.

---

## How I Verified the Work

I tested both valid and invalid scenarios for ticket assignments:

- Valid staff names successfully assign to existing ticket IDs and return the updated dictionary.
- Whitespace-padded names are trimmed and normalized correctly.
- Empty strings or non-string inputs raise a `ValueError`.
- Non-existent ticket IDs iterate through the full collection and raise a `KeyError`.

---

## Key Takeaway

I learned that backend workflow logic requires **strict defensive coding and explicit failure states**.

A reliable feature must **validate inputs early, avoid silent error returns, handle missing resources deterministically, and follow clean pull request workflows**.

AI guided my understanding of python exception mechanics and pull request resolution, while I remained responsible for writing, testing, and merging the code.