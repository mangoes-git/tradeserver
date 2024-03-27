start:
	uvicorn --app-dir server main:app --reload --loop asyncio