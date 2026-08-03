# Release Evidence

## Baseline

- Branch: `final-project`
- Date: 2026-08-03
- Local app run command: `uvicorn app.main:app --reload --port 8000` (documented host command; the runtime check below used the built image).
- /health result: HTTP `200`; `{"status":"ok","timestamp":"2026-08-03T15:35:53.679269+00:00"}`.
- Frontend check: served `frontend/` on port 5500 in a temporary container; `GET /` returned HTTP `200` and contained `Task Tracker`. The container was then removed.
- Test command: `$repoPath = (Get-Location).Path; docker run --rm --mount "type=bind,source=$repoPath,target=/src,readonly" --workdir /src --env PYTHONPATH=/src --env PYTHONDONTWRITEBYTECODE=1 task-tracker:dev pytest -v -p no:cacheprovider`
- Test result: `36 passed in 0.47s` on Python 3.11.15 with pytest 8.4.2.

## CI evidence

- Workflow file: `.github/workflows/ci.yml`; runs on push and pull request with Python 3.11 and installs `requirements.txt`.
- Latest run link or note: [GitHub Actions run 30752827403](https://github.com/Sarakarkaba/task-tracker-api/actions/runs/30752827403), completed successfully on 2026-08-02.
- Test command used by CI: `pytest -v`
- Shortcut check: no `continue-on-error` / no `|| true` / pytest is not skipped.

## Docker evidence

- Build command: `docker build -t task-tracker:dev .` - succeeded.
- Run command: `docker run --rm --name tt-release-evidence-20260803 -p 8000:8000 task-tracker:dev`
- /health check: `GET http://127.0.0.1:8000/health` returned HTTP `200` with status `ok` and a UTC timestamp.
- Non-root check, if implemented: `docker inspect` reported runtime user `app`; `Dockerfile` contains `USER app`.
- No-baked-secrets check: `.dockerignore` excludes `.env` and `.env.*`; `Dockerfile` copies only `requirements.txt` and `app/`, not the whole repository.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
| :--- | :--- | :--- | :--- |
| CI runs pytest on pushes and pull requests using Python 3.11. | `.github/workflows/ci.yml` | [Run 30748214278](https://github.com/Sarakarkaba/task-tracker-api/actions/runs/30748214278) failed; [run 30748564941](https://github.com/Sarakarkaba/task-tracker-api/actions/runs/30748564941) passed. | Added `PYTHONPATH: .` in commit `c4cf3f5` to fix the failed import. |
| The documented Docker build/run commands work and the container runs as non-root. | Successful local build, HTTP 200 runtime check, `docker inspect`, and `Dockerfile` | Confirmed. | None. |
| `/health` returns HTTP 200 with `status` and a UTC timestamp. | `app/main.py` and the running container response | `{"status":"ok","timestamp":"2026-08-03T15:24:06.600251+00:00"}` | None. |
