# Wavelength Recommendations

Starter repository for the Wavelength Recommendations mini-sprint.

## Setup

1. Fork and clone this repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create the Postgres database:
   ```bash
   createdb wavelength_recommendations
   ```
5. Create a `.env` file in the project root with:
   ```
   DATABASE_URL=postgresql://localhost/wavelength_recommendations
   ```
   Adjust the connection string for your local Postgres setup if needed.
6. Load the schema and seed data:
   ```bash
   psql wavelength_recommendations -f schema.sql
   psql wavelength_recommendations -f seed.sql
   ```
7. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

## Project structure

```
py-wavelength-recommendations/
├── main.py                    # FastAPI app and startup/shutdown of the connection pool
├── db.py                      # asyncpg connection pool and the get_async_conn dependency
├── routes/
│   └── recommendations.py     # the two existing endpoints
├── schema.sql                 # CREATE TABLE statements (already applied)
├── seed.sql                   # sample data (already applied)
├── NOTES.md                   # your write-up for whichever path you choose
└── requirements.txt
```

## What's already built

Both endpoints below are implemented and already async, using `asyncpg` - there is no blocking database code to convert here.

- `GET /recommendations/top-tracks/{genre}` - top tracks for a genre, ordered by play count
- `GET /recommendations/{user_id}` - a personalised feed for a given user, public, no authentication

Your mini-sprint task is to apply **one** of two improvements to this server - see your lesson instructions for the full brief:

- Apply a cache to the top-tracks endpoint
- Apply rate limiting to the per-user endpoint

## Data

The schema and seed data reuse the same Wavelength domain (artists, tracks, users, listening events) from the listening database sprint, with `genre` stored on `artists`.
