# SpyPlane

Scouting bot

# Functional Notes

[Link to Notes](https://docs.google.com/document/d/1a4U9vYSLk9_sQVjA3xz49KnCS0hibOq2ELEXc87X9yI/edit?usp=sharing)

# Tech Notes

## Local devbox setup

1. Install [poetry using instructions here](https://python-poetry.org/docs/#installation)
2. Optionally, configure poetry to create a virtualenv in project dir

```bash
poetry config virtualenvs.in-project true
```

3. `poetry install` the dependencies
4. Copy `.env.sample` to `.env` and update the values for TEST and PROD
5. Contact the dev team to get the token.json that allows connecting to Google Sheets API, 
and place it in the repo root.
6. Startup the bot with `poetry run spy`

## Google Drive Setup

Follow [gspread instructions](https://docs.gspread.org/en/latest/oauth2.html)
to connect to google sheet from your drive

