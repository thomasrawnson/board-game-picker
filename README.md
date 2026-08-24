# Board Game Picker

Board Game Picker is a mobile-first application for answering a familiar game-night question: **what should we play?**

The application imports a board game collection, stores game and play-history data in PostgreSQL, and recommends suitable games based on player count, available play time, complexity and recent play history.

It is also being developed as a data-engineering portfolio project, with an emphasis on ingestion, transformation, relational modelling, API design, testing and explainable recommendation logic.

## Current progress

Board Game Picker now has a working end-to-end application flow covering collection ingestion, recommendation, play tracking and collection analytics.

Currently implemented:

- React + TypeScript mobile-first frontend
- installable PWA support
- Python/FastAPI backend
- PostgreSQL 16 local development environment using Docker Compose
- SQLAlchemy persistence layer
- Alembic database migrations
- layered API, service and repository architecture
- BoardGameGeek XML API client and parsers
- retry handling for queued BoardGameGeek API responses
- BG Stats JSON collection ingestion
- BG Stats historical play ingestion
- idempotent play import using source identifiers
- game metadata including player counts, play time, complexity, ratings and artwork
- deterministic and explainable recommendation engine
- player-count and play-time filtering
- recommendation scoring informed by historical play recency
- game reveal interface using real BoardGameGeek artwork
- play-history recording from the frontend
- collection-insights API and React dashboard
- PostgreSQL aggregate queries for most played, last played and never played games
- automated tests across parsers, repositories, services and API endpoints

Development currently uses a BG Stats export as the primary source for collection and historical play data. BoardGameGeek integration is also available for collection and metadata synchronisation.

## Architecture

```text
React / TypeScript PWA
          |
          v
       FastAPI
          |
          v
  Application services
      /        \
     v          v
BGG / BG Stats  Repositories
                    |
                    v
                PostgreSQL
```

The backend uses a layered architecture so external clients, application logic and persistence remain separated.

```text
API
 |
Service
 |
Repository / External client
 |
PostgreSQL / BoardGameGeek / BG Stats
```

This keeps business logic independent of transport and persistence details and allows individual layers to be tested in isolation.

## Data ingestion

The application supports both BoardGameGeek XML and BG Stats JSON data flows.

```text
BoardGameGeek XML API ----> BGG parser --------\
                                               > Domain Game model
BG Stats JSON export ------> Collection parser /
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

Historical play data is imported separately from the same BG Stats export:

```text
BG Stats plays
      |
      v
Resolve gameRefId to BGG ID
      |
      v
Parse play date, players and duration
      |
      v
Deduplicate by source + play UUID
      |
      v
PostgreSQL plays table
```

The collection importer filters the export to currently owned games and uses the BGG ID as the stable game identifier. Re-importing collection data updates existing records instead of creating duplicates.

Historical plays are also idempotent: imported play UUIDs are stored with their source so repeated imports do not duplicate play records.

## Recommendation engine

The recommendation engine is deterministic and explainable rather than AI-driven.

Games are first filtered for eligibility using criteria such as:

- player count
- maximum play time
- maximum complexity
- ownership status

Eligible games are then ranked using a weighted score. Current scoring considers suitability against the selected criteria and historical play recency, allowing games that have not been played recently to rank above otherwise similar choices.

The API returns both the score and human-readable reasons so the frontend can explain why a game was recommended.

Example reasons include:

- `Supports 3 players`
- `Fits within 60 minutes`
- `Complexity 2.8 fits preference`
- `Hasn't been played in a while`

Play-history scoring will continue to be refined as the project develops.

## Collection insights

The application includes collection analytics backed by PostgreSQL aggregate queries.

Current insights include:

- total owned games
- total recorded plays
- most played games
- last played game
- games that have never been played

Historical BG Stats plays feed the same database used by the picker, so analytics and recommendations operate from a shared source of truth.

## Technology stack

### Backend

- **Python 3.12** — application, ingestion and transformation logic
- **FastAPI** — REST API and dependency injection
- **Pydantic** — request validation
- **SQLAlchemy** — ORM, sessions and database access
- **psycopg** — PostgreSQL driver
- **httpx** — BoardGameGeek HTTP client
- **pytest** — unit and integration testing

### Database and infrastructure

- **PostgreSQL 16** — relational application database
- **Alembic** — version-controlled schema migrations
- **Docker / Docker Compose** — reproducible local database environment

### Frontend

- **React**
- **TypeScript**
- **Vite**
- **vite-plugin-pwa** — installable mobile web application support

### Planned / next

- GitHub Actions CI/CD
- Azure deployment
- category and mechanic persistence
- similar-game discovery
- personal ranking
- richer recommendation scoring
- AI-assisted natural-language game filtering

## Testing

Testing is developed alongside each milestone rather than added at the end of the project.

The test suite covers areas including:

- BoardGameGeek HTTP client behaviour
- XML parsing
- BG Stats JSON parsing
- historical play parsing
- collection processing
- PostgreSQL connectivity
- repository CRUD operations
- service-layer behaviour
- recommendation scoring
- collection insights
- FastAPI endpoints

External dependencies are replaced with fakes, mocks or dependency overrides where appropriate so individual application layers can be tested independently.

Run the backend tests from `backend`:

```bash
python -m pytest
```

Check that SQLAlchemy models and Alembic migrations remain aligned:

```bash
alembic check
```

## Local development

### Prerequisites

- Python 3.12+
- Node.js
- Docker Desktop / Docker Compose

### Database

Start PostgreSQL from the repository root:

```bash
docker compose up -d
```

Apply database migrations from `backend`:

```bash
alembic upgrade head
```

The backend uses a `DATABASE_URL` environment variable. Local secrets and personal collection exports are intentionally excluded from source control.

### Backend

From `backend` with the virtual environment activated:

```bash
uvicorn api.main:app --reload
```

FastAPI's interactive API documentation is available at `/docs` on the local API server.

For local testing from another device on the same network, the API can be exposed on the local network:

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

From `frontend`:

```bash
npm install
npm run dev
```

For local mobile testing:

```bash
npm run dev -- --host
```

The frontend API URL can be configured using the `VITE_API_BASE_URL` environment variable.

Build the frontend with:

```bash
npm run build
```

## Roadmap

Near-term development priorities are:

1. Refine play-history-aware recommendation scoring
2. Persist categories and mechanics
3. Expand collection insights and play-history analytics
4. Add personal ranking and preference signals
5. Add similar-game discovery
6. Improve frontend component structure and mobile UX
7. Add GitHub Actions CI/CD
8. Add production configuration and observability
9. Deploy the frontend, API and database infrastructure to Azure
10. Explore AI-assisted natural-language filtering

## Project goals

The project is intended to demonstrate practical experience with:

- external API and file-based data ingestion
- XML and JSON parsing
- transformation into consistent domain models
- idempotent data loading
- source identifier mapping and deduplication
- relational data modelling
- PostgreSQL and SQL aggregation
- schema migration management
- Python application architecture
- REST API design
- automated testing
- Docker-based development
- explainable recommendation logic
- React and TypeScript frontend integration
- CI/CD and cloud deployment as later milestones

## Status

**Active development**

The core application is functional end to end: collection ingestion, PostgreSQL persistence, recommendation, play tracking and collection insights are implemented.

Current development is focused on improving recommendation quality, strengthening the mobile experience, and preparing the project for CI/CD and Azure deployment.
