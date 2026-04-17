# Lab Journal — Agent Instructions

Every session that changes code, specs, or design decisions **must** have a journal entry.

## Starting a Session

1. Copy `lab-journal/TEMPLATE.md` to `lab-journal/journal-YYYY-MM-DD.md` (append `b`, `c`, … for multiple sessions on the same day).
2. Fill in the date and session goals **before** starting work.

## During a Session

- Add sections as you work — never backfill from memory.
- Use tables for structured data: issues/fixes, test results, comparisons, before/after measurements.
- Fill in the **Hypothesis vs Measured Impact** table whenever changes are testable — state predictions *before* running, record actuals after.
- Include code snippets, error messages, and command output where they aid reproducibility.
- Record failures and rollbacks — they matter as much as successes.
- Note tool versions, model names, and environment details that affect results.

## Ending a Session

Fill in the footer block at the bottom of the entry:

- **Signed / Date** — full ISO timestamp
- **Participants & Tools** — model name, language version, key libraries
- **Commit / Witness** — git commit hash(es) + issue/bead IDs
- **Related Docs** — active spec versions and document paths referenced
- **Next journal entry** — next filename

## After Committing

Update `lab-journal/index.md` — add one row with date, file link, key topics, and milestone/phase. Keep the table chronological.

## Rules

- Entries are append-only. Never delete or rewrite. Add dated corrections referencing the original.
- Each entry must stand alone — enough detail for someone unfamiliar to reproduce the session.
- Link to commits and issues; don't redescribe what git already records.
- Attachments go in `lab-journal/attachments/` with date prefixes.
