# Final AI Review and Ownership Evidence

## AGENTS.md guardrails

- Repo-specific stack and commands included: yes
- Docs-first/read-first guardrail included: yes
- Unexpected app/frontend edits rule included: yes

## AI code review mini-log

Reviewed the real Docker change with `git show 99082b4 -- Dockerfile .dockerignore`.

| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
| :--- | :--- | :--- | :--- |
| Separate test-only packages from the runtime image instead of copying the full environment containing pytest and HTTPX. | Useful | `requirements.txt:6-7` and `Dockerfile:11-12,26` show that test packages enter the final image. | Verified against the diff; recorded as a low-severity image-minimization improvement, with no Module 5 app change. |
| Pin the Python base image and GitHub Actions by digest and add a security scanner now. | Noise | This is generic higher-assurance advice; no vulnerable artifact or course requirement was identified. | No change; reconsider only if the project gains production requirements. |
| `COPY . .` may copy `.env` secrets into the image. | Wrong | The Dockerfile does not use `COPY . .`; it copies only `requirements.txt` and `app/`, while `.dockerignore` excludes `.env` and `.env.*`. | Rejected after checking `Dockerfile` and `.dockerignore`; no change needed. |

## AI security mini-review

| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
| :--- | :--- | :--- | :--- | :--- |
| Task routes have no authentication or authorization. | `app/main.py:47-203`; `README.md:189-194` | Valid | This is acceptable for the local course scope but unsafe if the API is exposed to untrusted clients. | Keep the limitation documented; require an access-control design before deployment. |
| PATCH accepts explicit `null` for required response fields and returns HTTP 500. | `app/models.py:53-61`; `app/storage.py:149-163` | Valid | A pinned-image probe reproduced HTTP 500 for null `title`, `status`, and `priority`. | Add focused tests, then request approval for a minimal validation fix returning HTTP 422. |
| Missing `DELETE` from the CORS allowlist is a security vulnerability. | `app/main.py:24`; `frontend/index.html:740-850` | False Positive | The current frontend does not issue DELETE requests; a narrower unused-method allowlist is not a vulnerability. | None unless a cross-origin DELETE client is added. |
| Digest pinning and a security scanner are required for this course repository. | `.github/workflows/ci.yml`; `Dockerfile` | Noise | No concrete vulnerable dependency, unsafe effective permission, or failing course requirement was demonstrated. | No current change; reassess for a production release. |

## Manual security check

I checked the Docker build stages, copied paths, runtime user, health check, and command myself. `Dockerfile:26-36` copies only the Python environment and `app/`, switches to non-root user `app`, checks `/health`, and starts Uvicorn explicitly; `.dockerignore:1-3` excludes `.env` and `.env.*`. I found no additional secret-copy path in those Docker instructions, which matters because a broad build copy could bake local credentials into an image.

## One AI output I rejected or corrected

AI suggested that missing CORS permission for `DELETE` was a security defect. I did not accept it as-is because the current frontend never issues DELETE requests, and expanding the allowlist without a client requirement would weaken least privilege. I graded the suggestion False Positive and made no application change.

## Three AI usage rules

1. Never paste: credentials, environment values, personal data, private URLs, or unidentified external data.
2. Always verify: understand important generated lines and use focused tests, browser checks, CI/Docker inspection, or repository evidence appropriate to the change.
3. Record AI contributions by: naming what AI generated, the module, whether I understand it, the verification performed, and the final grade or decision.

## Ownership statement

I am comfortable submitting this project as my own because I understand how the API, in-memory storage, Kanban frontend, tests, CI, and Docker setup fit together. AI helped me draft and review parts of the work, but I checked its suggestions against the actual code and ran the relevant checks myself. I decided what to keep, corrected or rejected ideas that did not fit the assignment, and avoided adding features just because AI suggested them. I take responsibility for the final scope and the decisions reflected in this repository.
