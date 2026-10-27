# Baseline Check

## Scope and revision

The pre-change working tree was on `main` at `93d5f11` (`Merge pull request #21 from beze-123/feat/23-search-and-insights`). The task brief refers to an audited commit, but no audited commit hash or separate audit report was provided. Therefore, this records the available repository baseline; it does not claim that this revision is the audited revision.

## Run command and result

Command:

```bash
python -m unittest discover -s tests -v
```

Result before implementation changes: 21 tests ran; 19 passed and 2 errored. Both errors occurred when the CLI reached Search: `main.py` passed a `TicketStorage` object to `search_tickets`, which attempted to iterate it and raised `TypeError`.

A pytest run of the same baseline also reported 2 failures and 20 passes (8 subtests passed), for the same Search menu error.

## Inputs exercised by the baseline tests

These were scripted test interactions, not separate manual demonstrations:

1. Create a high-urgency Network ticket affecting 12 users, assign Alex, move it to `in_progress`, report it, resolve it, reopen it, then choose Search. The journey errored at Search.
2. Start with an unassigned open ticket, attempt to move it to `in_progress`, display the report, then choose Search. The transition was correctly rejected, but the journey errored at Search.
3. Search for the title substring `wifi` with category `Network`, status `open`, and priority `low`. This test lived under `tests/test/` and was not collected by the documented unittest discovery command. Its filter semantics were separately exercised with pytest.

## Audit observations

The supplied brief says the audit is preliminary peer feedback and lists the reliability areas to revisit: validation and lifecycle safety, notes, combined search, richer reports, safe JSON persistence, tests, and collaborative review. It does not include specific findings from an actual audit report. Do not represent that general checklist as confirmed peer findings; add the mentor's actual observations here when available.
