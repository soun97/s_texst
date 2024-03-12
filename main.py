from typing import Union

from fastapi import FastAPI
from datetime import datetime, timedelta

app = FastAPI()

last_heartbeat = datetime.now()

@app.get("/heartbeat")
def read_root():
    current_time = datetime.now()
    global last_heartbeat
    print("current : ", current_time)
    print("last : ", last_heartbeat)
    print("delta : ", current_time - last_heartbeat)
    if (current_time - last_heartbeat) < timedelta(seconds = 10):
        last_heartbeat = current_time
    else:
        # send telegram
        print("error")
    return "OK"


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}