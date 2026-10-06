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
| Task ID | 2 |
| Run 1 | 2166.16 ms |
| Run 2 | 2058.76 ms |
| Run 3 | 2734.10 ms |
| Run 4 | 2946.36 ms |
| Run 5 | 3464.47 ms |
| Median | 2734.10 ms (Target missed: > 200 ms) |
| Minimum / maximum | 2058.76 ms / 3464.47 ms (Spread: 1405.71 ms) |

Raw output was captured with five authenticated `Invoke-WebRequest` calls from Windows PowerShell to the local Docker-backed CVAT service. The target was missed in this environment; the endpoint query itself needs profiling before a performance claim can be made.
