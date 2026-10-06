# Annotation Analytics — Plan

## Goal

Add task-level annotation analytics to CVAT: an authenticated API that counts drawn shapes by class and a task analytics page that displays the counts as a bar chart.

## Work order

| Step | Work | Estimate |
| --- | --- | ---: |
| 1 | Record the CVAT SHA, create assessment documents, and commit them before code | 30 min |
| 2 | Import COCO data and verify visible annotations | 30 min |
| 3 | Inspect models, routing, authentication, permissions, and UI conventions | 45 min |
| 4 | Build the per-class shape-count endpoint | 75 min |
| 5 | Verify counts, authentication, and task access | 30 min |
| 6 | Replace the task analytics placeholder with the analytics UI | 60 min |
| 7 | Add bar chart, empty state, and retryable error state | 45 min |
| 8 | Measure five authenticated endpoint requests and record results | 30 min |
| 9 | Add a filter/grouping only if the core work is stable | 30 min |
| 10 | Final verification, documentation, cleanup, and recording preparation | 45 min |

Planned work is approximately seven hours; the remaining time is reserved for setup and debugging.

## Approach

The endpoint will be `GET /api/test/tasks/{task_id}/annotation-analytics`. It will reuse CVAT authentication and `TaskPermission`, count `LabeledShape` records through `shape.job -> job.segment -> task`, and return every configured task label with its count, including zeroes. Results will be sorted by label name.

The existing `/tasks/:tid/analytics` page and task-menu link will be reused. Its default paid-feature placeholder will be replaced with a Chart.js bar chart that calls the typed CVAT core client method. A task with no configured labels will show an empty state; a failed request will show an error state with retry.

## Deferred work

The optional filter/grouping and WebSocket live updates/recovery will not begin until the endpoint, graph, empty/error states, authorization checks, and performance measurement are complete. Any unfinished work will be documented honestly.

## Git sequence

The first commit contains only `docs/Plan.md`, `docs/Objectives.md`, and `docs/DefinitionOfDone.md`. Subsequent commits will isolate the backend endpoint, tests, UI, measurements, and final documentation.

Current CVAT SHA: `d8193c584be9ce6cf9882dad06c0dd920cc0b9c5`.
