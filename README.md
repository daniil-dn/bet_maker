## Setup & Run 🏃‍

```bash
docker-compose up --build

```

After first run:

1) docker exec -ti task_betting_software-app_line_provider-1 bash
2) docker network create bet-network
3) Run migrations
   alembic revision --autogenerate -m "Migration"
   alembic upgrade head
4) Run script to fill db with statuses
   python app/pre_start_fill_db.py
5) Run pytest - for testing

Test:
Для тестирования можно зайти в любой контейнер и запустить pytest

Комментарии:

1. Выбрал связь между микросервисами по http. Для коллбэков используется RabbitMQ

2. В качестве воркера для line_provider выбрал ARQ. Таски которые обрабатывают события хранятся в редисе. Исход события
   выбирается рандомно

   Visit  (http://localhost:9090/docs, http://localhost:9091/docs) for the interactive FastAPI docs!
