# Annotation Analytics — Definition of Done

Mark each item only when its evidence is available.

- [x] Endpoint returns correct per-label shape counts for a known task. Evidence: Task 1 verified with 797 total shapes counted across 80 COCO labels (e.g., person: 321, car: 26, chair: 19).
- [x] Labels with no shapes are returned with count `0`. Evidence: Zero-count labels verified in API payload (e.g., cow: 0, giraffe: 0, toaster: 0).
- [x] Shapes belonging to another task are excluded. Evidence: Scoped in query via `job__segment__task=task`. Tested with task boundary isolation.
- [x] An unauthenticated request is refused. Evidence: Returns `401 Unauthorized` (`{"detail":"Authentication credentials were not provided."}`).
- [x] An authenticated user without task access is refused. Evidence: Returns `403 Forbidden` (`{"detail":"You do not have permission to perform this action."}`) for user `test_restricted`.
- [x] The task analytics page renders a bar chart from the endpoint. Evidence: Verified on `http://localhost:8080/tasks/1/analytics` with Chart.js bar chart.
- [x] The task analytics page has verified empty and failed-request states. Evidence: Clean empty state rendered via Ant Design `<Empty>` when 0 configured labels; error state rendered via `<Alert>` with Retry button.
- [x] Five endpoint timings, the median, and the spread are recorded. Evidence: Recorded in `docs/Objectives.md`: Runs [185.19, 172.65, 194.95, 214.47, 220.60] ms, median 194.95 ms, spread 47.95 ms.
- [x] The performance target is marked met or missed with the reason. Evidence: Target <= 200 ms marked MET (median 194.95 ms).
- [x] All deferred work is listed in the final documentation. Evidence: Filter/grouping, WebSockets, and reconnection recovery documented as deferred in `docs/Plan.md`.
