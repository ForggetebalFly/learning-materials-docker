# Каталог учебных материалов
Автор: Демидов Д.М., группа 634. Задание 4.

Приложение Flask хранит каталог учебных материалов в JSON. Материалы можно просматривать, добавлять и удалять. Зависимости устанавливаются через Dockerfile.

## Запуск
```bash
docker compose up -d --build
```
Открыть http://localhost:8040 .
API: GET/POST `/api/resources`, DELETE `/api/resources/<id>`, GET `/health`.
Данные `/app/data/resources.json` копируются в образ и сохраняются в именованном томе при запуске через Compose.
Остановка: `docker compose down`. Для демонстрации после перезапуска том сохраняется.

## Проверка
```bash
python3 verify.py
python3 persistence.py create
docker compose down
docker compose up -d
python3 persistence.py check
```
Проверяются создание, чтение, удаление, ошибки 400 и 404 и сохранение записи после пересоздания контейнера.
