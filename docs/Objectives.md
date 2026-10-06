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
| CPU | Intel(R) Core(TM) i5-10310U CPU @ 1.70GHz (4 cores, 8 threads) |
| RAM | 16 GB |
| Operating system | Windows 11 Pro (Build 26300) / Docker Desktop (Linux containers) |
| CVAT commit SHA | `d8193c584be9ce6cf9882dad06c0dd920cc0b9c5` |
| COCO images imported | 100 images (from COCO 2017 validation set) |
| Task ID | 1 |
| Run 1 | 185.19 ms |
| Run 2 | 172.65 ms |
| Run 3 | 194.95 ms |
| Run 4 | 214.47 ms |
| Run 5 | 220.60 ms |
| Median | 194.95 ms (Target Met: <= 200 ms) |
| Minimum / maximum | 172.65 ms / 220.60 ms (Spread: 47.95 ms) |
