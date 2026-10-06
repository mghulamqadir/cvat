# Annotation Analytics — Objectives

## MO-1: authenticated endpoint response time

| Field | Entry |
| --- | --- |
| What is measured | Time for `GET /api/test/tasks/{task_id}/annotation-analytics` to return the per-label shape counts. |
| How | Five authenticated, warm requests against the local Docker stack; preserve raw timings from the measurement command. |
| Target | Median response time at or below 200 ms. |
| Conditions | Local Docker CVAT stack, imported COCO validation task, no intentional concurrent load. |
| Not included | Initial cold request, Docker startup, browser rendering, and WebSocket work. |

## Environment and results

Complete these fields after the sample task and endpoint exist.

| Field | Result |
| --- | --- |
| CPU | Pending measurement |
| RAM | Pending measurement |
| Operating system | Pending measurement |
| CVAT commit SHA | `d8193c584be9ce6cf9882dad06c0dd920cc0b9c5` |
| COCO images imported | Pending measurement |
| Task ID | Pending measurement |
| Run 1 | Pending measurement |
| Run 2 | Pending measurement |
| Run 3 | Pending measurement |
| Run 4 | Pending measurement |
| Run 5 | Pending measurement |
| Median | Pending measurement |
| Minimum / maximum | Pending measurement |
