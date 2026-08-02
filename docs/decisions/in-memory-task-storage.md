# Technical Decision: In-Memory Task Storage

**Status:** Accepted

## Context

The Task Tracker is a learning project built with FastAPI and Pydantic. It supports creating, listing, retrieving, updating, filtering, and deleting tasks. The route handlers in `app/main.py` delegate task operations to a separate storage module, while `app/models.py` defines the request and response shapes.

The project currently stores tasks in memory. This means that tasks are available only while the application process is running and are lost when the server or Docker container restarts.

The project does not have authentication, authorization, a database, deployment configuration, or production hardening. CI installs the Python dependencies and runs the tests on pushes and pull requests. The Docker image packages and runs the API, but it does not provide persistent storage or deploy the application.

## Decision

The Task Tracker will use process-local, in-memory storage for tasks.

A database or file-based persistence layer will not be added in this module. The existing storage boundary will continue to handle task creation, retrieval, updates, deletion, searching, and filtering.

This decision is appropriate for the current learning-project scope. It is not intended to be a production storage design.

## Alternatives Considered

### Relational database

SQLite or PostgreSQL could provide durable storage, transactions, and better support for multiple application processes.

This option was not selected because it would require database configuration, schema design, migrations, connection management, and additional testing. Those concerns would make the module more complex without being necessary for demonstrating the current API behavior.

### File-based storage

Tasks could be written to a JSON file so that they survive application restarts.

This would be simpler than introducing a full database, but it would create other problems. The application would need to handle interrupted writes, invalid file contents, and simultaneous access. It would also risk turning a temporary solution into an unreliable persistence layer.

### Managed database service

A hosted database could provide durable, shared storage and support a future deployed version of the application.

This option was not selected because the project has no deployment setup and is not presented as production-ready. Choosing a hosted service would also introduce decisions about credentials, networking, cost, backups, and security that are outside the scope of this module.

## Trade-offs

I kept the storage in memory because it let me focus on the parts I was actually trying to learn in this module: API behavior, validation, tests, CI, Docker, and documentation. I did not want database setup and migrations to become a separate project.

The biggest downside is that the data is temporary. If I stop the server or replace the container, every task disappears. That is acceptable for a course project, but it would be frustrating in an application that people expected to use regularly.

Another limitation is that the data belongs to one running application process. If the API were started with multiple worker processes, they would not automatically share the same tasks. I also have not confirmed how the storage implementation behaves when two requests try to update tasks at the same time.

The current approach keeps local setup and CI simple because neither one needs a database service. The cost of that simplicity is that persistence will have to be designed later if the project grows.

I would do this differently by defining a clearer storage interface from the beginning, so I could replace the in-memory implementation later without changing the API routes.

## Consequences

- Developers can run the API without installing or configuring a database.
- CI can run the tests without provisioning an external storage service.
- The Docker container can start without a database connection or mounted data volume.
- All task data is lost when the application process restarts.
- The application cannot currently provide durable or shared task state.
- Running more than one application process may create separate task collections.
- A future persistence layer will need to preserve the existing API response shapes unless an explicit API change is approved.
- Replacing the storage mechanism may be easier because the route handlers already call a separate storage module, but the strength of that separation should be checked in `app/storage.py`.
- This decision does not add authentication, authorization, deployment, backups, monitoring, or other production features.

## Open Questions

- When would losing tasks after a restart stop being acceptable for this project?
- If persistence is added, would SQLite be enough, or would the application need a shared database such as PostgreSQL?
- Can the current storage module be replaced without changing the route handlers or response models?
- How does the current storage code handle simultaneous requests?
- Should the API or frontend tell users that their tasks are temporary?
- Should task data be seeded for demonstrations, or should every run start empty?
