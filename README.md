# Task Tracker

A learning-project Task Tracker with a FastAPI backend and a browser-based
Kanban board built with vanilla HTML, CSS, and JavaScript.

The board supports task creation and editing, drag-and-drop status changes,
due dates, overdue filtering, text search, and combined filters.

## Requirements

- Python 3.10 or higher
- pip

## Setup

From the repository root, create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the application dependencies:

```powershell
python -m pip install -r requirements.txt
```

Install the test dependencies if they are not already available:

```powershell
python -m pip install pytest httpx
```

## Run the backend

From the repository root:

```powershell
python -m uvicorn app.main:app --reload
```

The API runs at `http://localhost:8000`. Interactive API documentation is
available at `http://localhost:8000/docs`.

## Run the frontend

Keep the backend running. In a second terminal, run:

```powershell
python -m http.server 5500 --directory frontend
```

Open `http://localhost:5500` in a browser. Use this URL and port so it matches
the backend's configured CORS origin.

## Run the tests

From the repository root:

```powershell
python -m pytest -q
```

To run the task API tests with detailed output:

```powershell
python -m pytest test/test_tasks.py -v
```
