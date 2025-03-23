How launch the project?

1) up containers by this command

       docker compose --env-file .template.env.docker up -d
2) make migrations

       docker exec -it app alembic --config app/alembic.ini upgrade head
3) load fixtures

       docker exec -it app python app/commands/load_fixtures.py
