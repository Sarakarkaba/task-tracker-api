# Module 5 Security Review

## Scope and Method

This review covers the Task Tracker backend, frontend, tests, dependencies,
CI workflow, and Docker configuration. I used AI for a read-only first pass,
then checked each finding against the repository and the available runtime
evidence. The final grades and decisions below are mine. No application code
was changed as part of this review.

The course labels used here are:

- **Valid**: the finding describes a real issue or limitation supported by evidence.
- **False Positive**: the finding misreads the current implementation or treats expected behavior as a defect.
- **Noise**: the suggestion may be reasonable in another context but is not supported as a current project issue.

## AI Findings and Final Grades

| ID | Severity stated by AI | Finding | File evidence | Risk | Final grade | My decision |
|---|---|---|---|---|---|---|
| SEC-01 | High if network-exposed | Task operations have no authentication, authorization, or ownership checks. | [`app/main.py:47-203`](../app/main.py#L47), [`README.md:189-194`](../README.md#L189), [`Dockerfile:36`](../Dockerfile#L36) | A client that can reach the API can read, create, change, or delete any task. | **Valid** | I accept this as a real deployment risk. It is allowed by the local course scope, so I documented it instead of adding authentication. It must be addressed before exposing the API to untrusted clients. |
| SEC-02 | Medium | Explicit `null` values for `title`, `status`, or `priority` can reach the non-null response model and return HTTP `500`. | [`app/models.py:53-61`](../app/models.py#L53), [`app/main.py:159-168`](../app/main.py#L159), [`app/storage.py:149-163`](../app/storage.py#L149) | Invalid client input produces a server error instead of a controlled validation response. | **Valid** | I reproduced the behavior with the pinned project dependencies. I kept it in the backlog because a fix would require focused tests and an explicitly approved application change. |
| SEC-03 | Medium if network-exposed | Description and assignee strings have no application-level length bounds, and the in-memory store and list endpoint have no task-count limit or pagination. | [`app/models.py:23-28`](../app/models.py#L23), [`app/main.py:72-79`](../app/main.py#L72), [`app/storage.py:14`](../app/storage.py#L14), [`app/storage.py:70`](../app/storage.py#L70), [`app/storage.py:101-112`](../app/storage.py#L101) | Repeated or oversized requests can increase memory use, processing work, and response size. | **Valid** | I accept this as a conditional resource-exhaustion risk. The in-memory design is appropriate for the course, but limits and pagination would be required for an externally exposed service. |
| SEC-04 | Medium if deployed | The frontend API URL and CORS allowlist are specific to the local HTTP workflow rather than a remote HTTPS deployment. | [`frontend/index.html:444`](../frontend/index.html#L444), [`app/main.py:21-26`](../app/main.py#L21), [`Dockerfile:36`](../Dockerfile#L36), [`README.md:189-194`](../README.md#L189) | A remote deployment would need an environment-specific API URL, approved origins, HTTPS, and access-control decisions. | **Valid** | I accept this as a deployment-readiness gap, not a defect in the documented local setup. I made no change because deployment is outside the project scope. |
| SEC-05 | Low | Actions, dependencies, and base images are not digest- or hash-pinned, and no security scan is configured. | [`.github/workflows/ci.yml:1-28`](../.github/workflows/ci.yml#L1), [`requirements.txt`](../requirements.txt), [`Dockerfile:1-15`](../Dockerfile#L1) | Mutable upstream artifacts can create provenance risk in a higher-assurance workflow. | **Noise** | I am not treating generic digest pinning or scanner adoption as a current course defect because no vulnerable artifact, unsafe effective permission, or failing requirement was demonstrated. I would reassess this for a real production release. |
| SEC-06 | Low | Test dependencies are copied into the runtime image. | [`requirements.txt:6-7`](../requirements.txt#L6), [`Dockerfile:11-12`](../Dockerfile#L11), [`Dockerfile:26`](../Dockerfile#L26) | Unneeded packages increase image size and the amount of installed runtime software. | **Valid** | I accept this as a concrete image-minimization issue. The current image still works and runs as non-root, so I recorded a future dependency split rather than changing the Docker design during Module 5. |
| SEC-07 | Informational | Missing `DELETE` from the CORS allowlist was reported as a security vulnerability. | [`app/main.py:21-25`](../app/main.py#L21), [`app/main.py:177-203`](../app/main.py#L177), [`frontend/index.html:776-835`](../frontend/index.html#L776) | The current frontend does not make cross-origin `DELETE` requests, so the narrower allowlist does not break a current client or create a security weakness. | **False Positive** | I rejected this finding. Expanding the allowlist without a client requirement would weaken least privilege; I would add `DELETE` only if a trusted cross-origin client actually needed it. |

## Verification Performed

On 2026-08-04, I checked SEC-02 inside the existing `task-tracker:dev`
container image. The image uses the versions pinned by this repository:
FastAPI `0.115.12` and Pydantic `2.11.4`. A FastAPI `TestClient` probe with
server exceptions disabled returned HTTP `500` for each of these PATCH bodies:

- `{"title": null}`
- `{"status": null}`
- `{"priority": null}`

I also ran the task API suite from the same image against the current
read-only working tree:

```powershell
$repoPath = (Get-Location).Path
docker run --rm --mount "type=bind,source=$repoPath,target=/src,readonly" --workdir /src --env PYTHONPATH=/src --env PYTHONDONTWRITEBYTECODE=1 task-tracker:dev pytest test/test_tasks.py -q -p no:cacheprovider
```

Result: `36 passed in 0.82s`.

These runtime checks support the code review, but they do not replace the
separate manual inspection below.

## My Manual Security Check

I manually checked the Docker build stages, copied paths, runtime user, health
check, and startup command. The final stage copies the Python environment and
the `app/` directory instead of copying the whole repository. It switches to
the non-root `app` user, checks `/health`, and starts Uvicorn explicitly.
I also checked `.dockerignore` and confirmed that it excludes `.env` and
`.env.*` files.

I did not find an additional path in these Docker instructions that would copy
a local secret into the image. This matters because a broad build-context copy
could silently bake credentials into an image. My check also confirmed the AI
finding that the complete Python environment includes test packages in the
runtime stage, which is unnecessary but low severity for this course image.

## Reconciliation

| Agreement between AI and me | AI-only findings | My additional manual result |
|---|---|---|
| We agreed that test dependencies enter the runtime image (SEC-06) and that the Docker runtime otherwise uses scoped copies and a non-root user. | AI identified the access-control, PATCH-null, resource-limit, local-deployment, supply-chain, and CORS questions. I graded each against code or runtime evidence rather than accepting it automatically. | My Docker inspection found no additional secret-copy path. This was a clean check, not a new vulnerability. |

The comparison changed the answer in two places: I classified the generic
supply-chain hardening request as **Noise** for the current scope, and I
rejected the missing-`DELETE` CORS claim as a **False Positive**.

## Top-3 Security Backlog

This backlog contains the highest-priority findings currently graded Valid.
It records future work and does not authorize application changes during
Module 5.

| Rank | Finding | Why it matters | Suggested owner | Next action |
|---:|---|---|---|---|
| 1 | SEC-01: no authentication, authorization, or ownership checks | Any reachable client can operate on every task; the risk becomes high outside the trusted course environment. | Course/project owner | Keep the limitation documented and require an approved access-control design before deployment. |
| 2 | SEC-02: nullable required PATCH fields return `500` | Invalid client input should be rejected rather than reaching an incompatible response model. | Backend | Add focused regression tests for the three fields, then request approval for the smallest validation fix returning HTTP `422`. |
| 3 | SEC-03: unbounded inputs, task count, and list responses | Repeated or oversized requests can increase memory use and response work. | Backend | Define description and assignee limits, a task-capacity policy, and pagination requirements before production use. |

## AI Output Corrected or Rejected

- I downgraded SEC-05 to **Noise** because the original audit presented generic
  supply-chain hardening without demonstrating a vulnerable dependency,
  unsafe effective permission, or repository failure.
- I graded SEC-07 as a **False Positive** because the current browser client
  does not use `DELETE`, and a narrower CORS method list is not itself a
  security defect.
- I rejected a separate claim that `COPY . .` might add `.env` secrets to the
  image. The Dockerfile does not use `COPY . .`; it copies only
  `requirements.txt` and `app/`, while `.dockerignore` excludes `.env` files.

## Files Used as Evidence

- Backend: `app/main.py`, `app/models.py`, `app/storage.py`, and
  `app/business_rules.py`.
- Tests: `test/conftest.py` and `test/test_tasks.py`.
- Frontend: `frontend/index.html`.
- Delivery and dependencies: `requirements.txt`, `Dockerfile`,
  `.dockerignore`, and `.github/workflows/ci.yml`.
- Scope and retained evidence: `README.md`, `AGENTS.md`,
  `docs/release-evidence.md`, and `docs/final-ai-review.md`.

## Limits and Production Readiness

- No external dependency vulnerability scan was run, so current dependency
  vulnerability status is **not confirmed**.
- Firewall, reverse-proxy, cloud, GitHub repository, and branch-protection
  settings were not inspected and are **not confirmed**.
- The targeted PATCH probe confirms the current failure behavior but does not
  fix it; SEC-02 remains open.
- The project is a local course application, not a production deployment.
  Because Valid findings remain, especially missing access control, the review
  does not claim that the application is production-ready.
- No backend, frontend, CI, or Docker changes were made during this review.
