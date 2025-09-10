from fastapi import FastAPI, WebSocket
import asyncio
from sql_agent import run_sql_query

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/hello/{name}")
def read_item(name: str):
    return {"message": f"Hello, {name}!"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Jalankan query SQL di thread terpisah karena agent.invoke synchronous
            response = await asyncio.to_thread(run_sql_query, data)
            await websocket.send_text(str(response))
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()