start:
		docker compose up -d
start-dev:
		uvicorn --app-dir server main:app --reload --loop asyncio
watch-logs:
		docker logs webhook-server --tail=20 -f
stop:
		docker compose down