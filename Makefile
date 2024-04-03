start:
		docker compose up -d
start-dev:
		uvicorn --app-dir server main:app --reload --loop asyncio
watch-server:
		docker logs webhook-server --tail=50 -f
watch-ib:
		docker logs webhook-trader-ib-gateway-1 --tail=100 -f
stop:
		docker compose down