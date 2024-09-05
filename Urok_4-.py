from fastapi import FastAPI, Body, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
from fastapi.templating import Jinja2Templates

app = FastAPI

templates = Jinja2Templates(directory="templates")

message_db = []


class Message(BaseModel):
    id: int = None
    text: str


@app.get(path="/", response_model=List[Message])
def get_all_message(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("message.html", {"request": request, "messages": message_db})


@app.get(path="/message/{message_id}")
def get_message(request: Request, message_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse("message.html", {"request": request, "message": message_db[message_id]})
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found")


@app.post("/message")
def create_message(message: Message) -> str:
    message.id = len(message_db)
    message_db.append(message)
    return "Message created!"


@app.put("/message/{message_id}")
def update_message(message_id: int, message: str = Body()) -> str:
    try:
        edit_message = message_db[message_id]
        edit_message.text = message
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found!")


@app.delete("/message/{message_id}")
def delete_message(message_id: int) -> str:
    try:
        message_db.pop(message_id)
        return f"Message_ID={message_id} deleted!"
    except IndexError:
        raise HTTPException(status_code=404, detail="Message not found!")


@app.delete("/")
def kill_all() -> str:
    message_db.clear()
    return "ALL MESSAGE DELETED!"