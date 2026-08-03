# Governance Retrospective - AI-Assisted Coding

## What I Shared With AI

| Item shared | Risk | Reason | Safer future version | Resolution or remaining limit |
|---|---|---|---|---|
| Task Tracker code | Low | This is course-project code, and I did not identify credentials, personal records, or production configuration in the material shared. | Share only the files or snippets needed after checking them for secrets and personal data. | The repository's public/private status is not confirmed, so I will treat its code as private by default. |
| Test output and stack traces | Medium | Diagnostic output can expose implementation details and local paths, including my local username. | Share only the relevant error and replace local paths, usernames, IDs, and secrets with placeholders. | I identified local-path disclosure as the main issue; no credential or environment-value disclosure is recorded. |
| Frontend code | Low | The frontend uses course sample data and a localhost API URL; I did not identify real user data or private endpoints in the material shared. | Share only the relevant function or UI state and replace private URLs or sample identities. | No real external dataset was identified. |
| Dockerfile and CI YAML | Low | These files contain course configuration and no production registry, account, or secret values were identified. | Replace private registries, URLs, account names, and secret names with placeholders before sharing. | Repository inspection confirmed that the Dockerfile copies only `requirements.txt` and `app/`, while `.dockerignore` excludes `.env` files. |
| Real external data | Not applicable | I did not identify a real external dataset used or shared during this project. | Continue using fabricated or anonymized data that preserves only the structure needed for the task. | If real data is needed later, confirm its source, sensitivity, and sharing authorization before using AI. |

## What I Received From AI

| Generated thing | Module | Do I understand it line by line? | Verification performed and decision |
|---|---:|---|---|
| Backend models and validators | 2 | Yes | I reviewed the fields and validators against the API behavior. The release check ran the full suite with Python 3.11 and recorded `36 passed`. I accepted the implementation while retaining the documented PATCH-null limitation for follow-up. |
| Frontend board and drag-and-drop logic | 3 | Yes | I traced the relevant event handlers and state updates. The retained release check confirms that the frontend served successfully and contained the Task Tracker page; it does not independently prove every browser interaction. |
| CI workflow | 4 | Yes | I inspected the triggers, Python version, dependency installation, and pytest command. I kept the workflow after a failed run exposed the missing import path, commit `c4cf3f5` corrected it, and a later GitHub Actions run passed. |
| Dockerfile | 4 | Yes | I reviewed both build stages, copied paths, runtime user, health check, and command. The image built, `/health` returned HTTP `200`, and inspection confirmed the runtime user is `app`. I accepted the design and recorded test packages in the runtime image as a low-severity improvement. |
| Security findings and plans | 5 | Yes | I checked the findings against repository and runtime evidence. I kept missing access control and PATCH-null handling as **Valid**, rejected the DELETE CORS claim as a **False Positive**, and classified mandatory digest pinning/scanning as **Noise** for the current course scope. No application change was authorized. |

## Evidence References

- [`docs/release-evidence.md`](release-evidence.md): test, CI, frontend-serving, Docker, health, and non-root evidence.
- [`docs/final-ai-review.md`](final-ai-review.md): final AI-review and security classifications, manual Docker security check, and ownership statement.
- [`docs/ai-usage.md`](ai-usage.md): the personal rules used to evaluate sharing, verification, and record keeping.
