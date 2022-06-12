# SpyPlane
Scouting bot

# Tech Notes

## Local devbox setup 
1. Install poetry
2. Optionally, configure poetry to create a virtualenv in project dir
```bash
poetry config virtualenvs.in-project true
```
3. Poetry install the dependencies
4. Copy `.env.sample` to `.env` and update the values for TEST and PROD
5. Startup the bot with `poetry run spy`
