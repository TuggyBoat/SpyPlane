# SpyPlane

Scouting bot

# Tech Notes

## Local devbox setup

1. Install [poetry using instructions here](https://python-poetry.org/docs/#installation)
2. Optionally, configure poetry to create a virtualenv in project dir

```bash
poetry config virtualenvs.in-project true
```

3. `poetry install` the dependencies
4. Copy `.env.sample` to `.env` and update the values for TEST and PROD
5. Startup the bot with `poetry run spy`

## Google Drive Setup

Follow [gspread instructions](https://docs.gspread.org/en/latest/oauth2.html)
to connect to google sheet from your drive

