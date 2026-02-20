from fastapi import FastAPI, HTTPException, Request, status 
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel 
import uvicorn  
import random
import requests
import json 

first = random.randint(1, 1000000000)

SESSION_FILE = Path("session.json")
templates = Jinja2Templates(directory="templates")
app = FastAPI()


def load_session() -> dict:
    if not SESSION_FILE.is_file():
        SESSION_FILE.write_text("{}")
    try:
        with SESSION_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Failed to decode session data from {SESSION_FILE}") from exc


def save_session(data: dict) -> None:
    try:
        with SESSION_FILE.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as exc:
        raise RuntimeError(f"Failed to save session data to {SESSION_FILE}") from exc

session = load_session()

class Card(BaseModel):
    tcg: str
    card_id: str
    card_name: str
    image: Optional[str] = None


@app.get("/")
def home(request: Request):
    regen = random.randint(1, 1000000000)
    return templates.TemplateResponse("index.html", {"request": request, "name": "Welcome", "background": "grey", "color": "green", "regen": regen, "first": first})
@app.get("/gallery")
def home(request: Request):
    return templates.TemplateResponse("gallery.html", {"request": request, "name": "", "background": "grey", "color": "green",})
@app.get("/about")
def home(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "name": "", "background": "grey", "color": "green",})
@app.get("/contact")
def home(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request, "email": "snider@snider.com", "background": "grey", "color": "green",})
@app.get("/add")
def add(a: float, b: float):
    return {"result": a + b}
@app.get('/get_website')
def get_website():
    response = requests.get('https://www.tcgplayer.com/product/554977/yugioh-battles-of-legend-terminal-revenge-dragon-master-magia-quarter-century-secret-rare?page=1&Language=English&utm_campaign=20486200459&utm_source=google&utm_medium=cpc&utm_content=703416088519&utm_term=&adgroupid=161217872788&gad_source=1&gad_campaignid=20486200459&gclid=Cj0KCQiAp-zLBhDkARIsABcYc6u_oywdr4UV9ZP_ci3Pc0fkygd0lc159bfBVE3VPlmaqcvA_w3OspYaAgjlEALw_wcB')
    return HTMLResponse(
        content=response.text,
        status_code=200,
        headers={}
    )

@app.post("/add_cards", response_model=Card)
def add_card(
    tcg: str,
    card_name: str,
    card_id: str,
    image: Optional[str] = None,
):
    card = Card(tcg=tcg, card_id=card_id, card_name=card_name, image=image)

    cards: List[dict] = session.setdefault(card.tcg, [])
    if any(c["card_id"] == card.card_id for c in cards):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Card with this ID already exists for the given TCG",
        )
    cards.append(card.dict())
    save_session(session)
    return card

@app.get("/search_cards")
def search_cards(
    tcg: str,
    card_name: Optional[str] = None,
    card_id: Optional[str] = None,
):
    stored = session.get(tcg, [])
    results = [
        c
        for c in stored
        if (card_name is None or c["card_name"] == card_name)
        and (card_id is None or c["card_id"] == card_id)
    ]
    return JSONResponse(content=results)

@app.delete("/delete_cards")
def delete_card(tcg: str, card_id: str):
    cards: List[dict] = session.get(tcg, [])
    new_cards = [c for c in cards if c["card_id"] != card_id]
    if len(new_cards) == len(cards):
        raise HTTPException(status_code=404, detail="Card not found")
    session[tcg] = new_cards
    save_session(session)
    return {"detail": "Card deleted"}

def _ensure_user(username: str) -> dict:
    users = session.setdefault("users", {})
    if username not in users:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found")
    return users[username]


@app.post("/users/{username}", status_code=status.HTTP_201_CREATED)
def create_user(username: str):
    users = session.setdefault("users", {})
    if username in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User '{username}' already exists",
        )
    users[username] = {}         
    save_session(session)
    return {"detail": f"User '{username}' created"}


@app.get("/users")
def list_users():
    users = session.get("users", {})
    return {"users": list(users.keys())}


@app.post("/users/{username}/cards", response_model=Card, status_code=status.HTTP_201_CREATED)
def add_card_to_user(
    username: str,
    tcg: str,
    card_id: str,
):
    user_collection = _ensure_user(username)
    main_cards: List[dict] = session.get(tcg, [])
    card_data = next((c for c in main_cards if c["card_id"] == card_id), None)
    if card_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Card '{card_id}' not found in main database for TCG '{tcg}'",
        )
    user_refs: List[dict] = user_collection.setdefault(tcg, [])
    if any(r["card_id"] == card_id for r in user_refs):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Card already in user's collection",
        )

    user_refs.append({"card_id": card_id, "tcg": tcg})
    save_session(session)
    return Card(**card_data)


@app.get("/users/{username}/cards")
def search_user_cards(
    username: str,
    tcg: str,
    card_name: Optional[str] = None,
    card_id: Optional[str] = None,
):
    user_collection = _ensure_user(username)
    user_refs: List[dict] = user_collection.get(tcg, [])
    user_card_ids = {r["card_id"] for r in user_refs}
    main_cards: List[dict] = session.get(tcg, [])
    results = [
        c for c in main_cards
        if c["card_id"] in user_card_ids
        and (card_name is None or c["card_name"] == card_name)
        and (card_id is None or c["card_id"] == card_id)
    ]

    return JSONResponse(content=results)


@app.delete("/users/{username}/cards")
def delete_user_card(username: str, tcg: str, card_id: str):
    user_collection = _ensure_user(username)
    refs: List[dict] = user_collection.get(tcg, [])
    new_refs = [r for r in refs if r["card_id"] != card_id]
    if len(new_refs) == len(refs):
        raise HTTPException(status_code=404, detail="Card not found in user's collection")

    user_collection[tcg] = new_refs
    save_session(session)
    return {"detail": "Card removed from user's collection"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)