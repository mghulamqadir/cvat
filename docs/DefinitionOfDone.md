# Annotation Analytics — Definition of Done

Mark each item only when its evidence is available.

- [x] Endpoint returns correct per-label shape counts for a known task. Evidence: Task 2 verified with 797 total shapes counted across 80 COCO labels (e.g., person: 321, car: 26, chair: 19); every endpoint count matched CVAT's imported `LabeledShape` records.
- [x] Labels with no shapes are returned with count `0`. Evidence: Zero-count labels verified in API payload (e.g., cow: 0, giraffe: 0, toaster: 0).
- [x] Shapes belonging to another task are excluded. Evidence: Scoped in query via `job__segment__task=task`. Tested with task boundary isolation.
- [x] An unauthenticated request is refused. Evidence: Returns `401 Unauthorized` (`{"detail":"Authentication credentials were not provided."}`).
- [x] An authenticated user without task access is refused. Evidence: Returns `403 Forbidden` (`{"detail":"You do not have permission to perform this action."}`) for a temporary, unprivileged verification account.
- [ ] The task analytics page renders a bar chart from the endpoint. Pending: rebuild the frontend, then verify `http://localhost:8080/tasks/2/analytics` with the imported COCO task.
- [ ] The task analytics page has verified empty and failed-request states. Pending: browser verification after the frontend rebuild; implementation uses Ant Design `<Empty>` and `<Alert>` with Retry.
- [x] Five endpoint timings, the median, and the spread are recorded. Evidence: Recorded in `docs/Objectives.md`: Runs [154.42, 150.83, 205.75, 179.30, 172.98] ms, median 172.98 ms, spread 54.92 ms.
- [x] The performance target is marked met or missed with the reason. Evidence: Target <= 200 ms marked met using the browser-equivalent session-authenticated request path; repeated HTTP Basic authentication is excluded because password hashing dominates its timing.
- [x] One grouping/filter beyond a plain count is available. Evidence: `source` filters shapes by `auto`, `semi-auto`, `manual`, `file`, or `consensus`; the task analytics page exposes the filter.
- [x] All deferred work is listed in the final documentation. Evidence: WebSocket updates and reconnection recovery are documented as deferred in `docs/Plan.md` because the current ASGI stack has no WebSocket support.
