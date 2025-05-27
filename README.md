How launch the project?

1) up containers by this command

       docker compose --env-file .template.env.docker up -d
2) make migrations

       docker exec -it app alembic --config app/alembic.ini upgrade head
3) load fixtures

       docker exec -it app python app/commands/load_fixtures.py

To see the result follow this link http://0.0.0.0:8000/docs


В файле .template.env можно настроить время диапазона для поиска лекарств ближайшего приема
# app config
FASTAPI__RANGE_TIME=6
