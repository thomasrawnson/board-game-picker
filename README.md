# Board Game Picker

> **Work in progress** — a mobile-first board game recommendation application and data-engineering portfolio project.

Board Game Picker is being built to answer a familiar game-night problem: **what should we play?**

The application imports a board game collection, stores and enriches game metadata, and will recommend suitable games based on factors such as player count, available play time, complexity and user preferences.

The project is also designed as a practical portfolio project demonstrating Python, data ingestion, API development, relational modelling, automated testing, containerisation and cloud deployment.

## Current progress

The backend foundation and collection ingestion flow are under active development.

Currently implemented:

- React + TypeScript frontend foundation using Vite
- Python/FastAPI backend
- BoardGameGeek XML API client and parsers
- Retry handling for queued BGG API responses
- Domain `Game` model
- PostgreSQL local development environment using Docker Compose
- SQLAlchemy database integration
- Repository CRUD operations
- Service layer separating business logic from persistence
- FastAPI game endpoints with Pydantic validation
- Collection sync API endpoint
- Automated tests using pytest, fixtures and dependency overrides
- BG Stats JSON collection parser
- BG Stats collection import into PostgreSQL
- Idempotent create/update behaviour when importing an existing collection

A live BoardGameGeek collection sync is planned once API token access is available. In the meantime, development uses a Board Game Stats JSON export as an additional ingestion source.

## Architecture

```text
React / TypeScript
        |
        v
     FastAPI
        |
        v
 Application services
    /          \
   v            v
BGG / BG Stats  Repository
                    |
                    v
                PostgreSQL
```

The backend uses a layered architecture so external APIs, application logic and database persistence remain separated.

```text
API
 |
Service
 |
Repository / External clients
 |
PostgreSQL / BoardGameGeek
```

This allows components to be tested independently and means application logic does not need to know the details of SQLAlchemy or the external data source.

## Data ingestion

The application currently supports two collection-data paths:

```text
BoardGameGeek XML API ----> BGG parser -----\
                                           > Domain Game model
BG Stats JSON export ------> JSON parser ---/
                                                   |
                                                   v
                                             Import service
                                                   |
                                                   v
                                               Repository
                                                   |
                                                   v
                                              PostgreSQL
```

The BG Stats importer filters the export to currently owned games and uses the BGG ID as the stable game identifier. Re-importing the same collection updates existing records instead of creating duplicates.

## Technology stack

### Backend

- **Python 3.12** — application, ingestion and data-processing logic
- **FastAPI** — REST API and dependency injection
- **Pydantic** — request validation
- **SQLAlchemy** — ORM, sessions and database access
- **psycopg** — PostgreSQL driver
- **httpx** — BoardGameGeek HTTP client
- **pytest** — unit and integration testing

### Database & infrastructure

- **PostgreSQL 16** — relational application database
- **Docker / Docker Compose** — reproducible local database environment

### Frontend

- **React**
- **TypeScript**
- **Vite**

### Planned

- Alembic database migrations
- GitHub Actions CI/CD
- Azure deployment
- Recommendation/scoring engine
- Play history and collection statistics
- AI-assisted natural-language game filtering

## Testing

Testing is being added alongside each milestone rather than left until the end of the project.

The test suite covers areas including:

- BGG HTTP client behaviour
- XML parsing
- BG Stats JSON parsing
- collection processing
- PostgreSQL connectivity
- repository CRUD operations
- service-layer behaviour
- FastAPI endpoints

External dependencies are replaced with fakes/mocks where appropriate so individual application layers can be tested independently.

Run the backend tests from `backend`:

```bash
python -m pytest
```

## Local development

### Prerequisites

- Python 3.12+
- Node.js
- Docker Desktop / Docker Compose
- PostgreSQL runs through the provided Docker Compose configuration

### Database

Start PostgreSQL from the repository root:

```bash
docker compose up -d
```

The backend uses a `DATABASE_URL` environment variable. Local secrets and personal collection exports are intentionally excluded from source control.

### Backend

From `backend` with the virtual environment activated:

```bash
uvicorn api.main:app --reload
```

FastAPI's interactive API documentation is then available at `/docs` on the local API server.

### Frontend

From `frontend`:

```bash
npm install
npm run dev
```

## Roadmap

Near-term development priorities are:

1. Expand the PostgreSQL game schema to retain richer collection metadata
2. Introduce Alembic migrations for version-controlled schema changes
3. Complete resilient collection synchronisation and error handling
4. Model collections, categories and mechanics
5. Build the game picker and explainable recommendation score
6. Develop the mobile-first tabletop UI
7. Add play history, rankings and collection statistics
8. Add similar-game discovery
9. Add CI/CD and observability
10. Deploy the application to Azure

## Recommendation concept

The first recommendation engine will be deterministic and explainable rather than AI-driven.

Potential inputs include:

- player count
- available play time
- complexity
- category/mechanic preferences
- game rating
- user ranking
- recent play history
- variety

The UI will expose this as a match score, for example **92% MATCH**, with the ability to explain why a game was recommended.

AI may later be used to translate natural-language requests such as:

> Four of us have about 90 minutes and want something competitive but not too heavy.

into structured filters consumed by the normal recommendation engine.

## Project goals

Beyond producing a useful application, this project is intended to demonstrate:

- external API ingestion
- transformation of XML/JSON into consistent domain models
- idempotent data loading
- relational data modelling
- PostgreSQL and SQL
- Python application architecture
- API design
- testing strategy
- Docker-based development
- CI/CD
- cloud deployment
- explainable recommendation logic

## Status

🚧 **Active development**

The architecture and data layer are currently the main focus. The README will evolve alongside the project as the picker UI, recommendation engine, CI/CD and cloud deployment are completed.
