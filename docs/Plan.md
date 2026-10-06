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

The endpoint will be `GET /api/test/tasks/{task_id}/annotation-analytics`. It will reuse CVAT authentication and `TaskPermission`, count `LabeledShape` records through `shape.job -> job.segment -> task`, and return every configured task or project label, including sublabels and zeroes. Results will be sorted by label name. An optional `source` query parameter provides the selected grouping/filter beyond the plain count.

The existing `/tasks/:tid/analytics` page and task-menu link will be reused. Its default paid-feature placeholder will be replaced with a Chart.js bar chart that calls the typed CVAT core client method. A task with no configured labels will show an empty state; a failed request will show an error state with retry.

## Deferred work

WebSocket live updates and reconnection recovery are deferred. The current CVAT ASGI application has no WebSocket routing or Django Channels dependency; implementing this safely requires an infrastructure change rather than a page-only change. Any unfinished work is documented honestly.

## Git sequence

The first commit contains only `docs/Plan.md`, `docs/Objectives.md`, and `docs/DefinitionOfDone.md`. Subsequent commits will isolate the backend endpoint, tests, UI, measurements, and final documentation.

## Decision record

* **Approach taken**: Direct database-level aggregation in PostgreSQL using Django ORM (`values("label_id").annotate(count=Count("id"))`).
* **Approach rejected**: Fetching all task annotations into Python memory or delegating the count to client-side JavaScript.
* **Cost of rejecting**: Fetching raw annotation records incurs substantial memory overhead in worker processes and serializes large payloads over the network. Rejecting this saved hundreds of milliseconds in transfer time and memory, but limits the current count to shapes rather than tracks.

Current CVAT SHA: `d8193c584be9ce6cf9882dad06c0dd920cc0b9c5`.
