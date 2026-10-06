# Annotation Analytics — Objectives

## MO-1: authenticated endpoint response time

| Field | Entry |
| --- | --- |
| What is measured | Time for `GET /api/test/tasks/{task_id}/annotation-analytics` to return the per-label shape counts. |
| How | Five authenticated, warm session-cookie requests against the local Docker stack; preserve raw timings from the measurement command. |
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
| Run 1 | 154.42 ms |
| Run 2 | 150.83 ms |
| Run 3 | 205.75 ms |
| Run 4 | 179.30 ms |
| Run 5 | 172.98 ms |
| Median | 172.98 ms (Target met: <= 200 ms) |
| Minimum / maximum | 150.83 ms / 205.75 ms (Spread: 54.92 ms) |

Raw output was captured with five authenticated `Invoke-WebRequest` calls from Windows PowerShell to the local Docker-backed CVAT service. Session authentication matches the browser UI. Repeating HTTP Basic authentication was deliberately excluded because its password-hash verification added 1.7–3.1 seconds per request; the endpoint's database aggregation itself measured 33.53 ms inside the CVAT container.
