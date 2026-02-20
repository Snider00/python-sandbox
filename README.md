# TCG Card Collection API

A FastAPI-based REST API for managing trading card game (TCG) collections. Supports a global card database and per-user card collections.

---

## Getting Started

**Install dependencies:**
```bash
pip install fastapi uvicorn requests pydantic
```

**Run the server:**
```bash
python main.py
```

The API will be available at `http://127.0.0.1:8000`. Interactive docs at `http://127.0.0.1:8000/docs`.

---

## API Endpoints

### Global Card Database

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/add_cards` | Add a card to the main database |
| `GET` | `/search_cards` | Search cards by TCG, name, or ID |
| `DELETE` | `/delete_cards` | Delete a card from the main database |

**Add a card:**
```
POST /add_cards?tcg=yugioh&card_name=Dark Magician&card_id=46986414&image=<url>
```

**Search cards:**
```
GET /search_cards?tcg=yugioh&card_name=Dark Magician
```

---

### User Collections

Users hold **references** to cards in the global database — card data lives in one place.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/users/{username}` | Create a new user |
| `GET` | `/users` | List all users |
| `POST` | `/users/{username}/cards` | Add a card from the main DB to a user's collection |
| `GET` | `/users/{username}/cards` | Search a user's card collection |
| `DELETE` | `/users/{username}/cards` | Remove a card from a user's collection |

**Create a user:**
```
POST /users/ash
```

**Add a card to a user's collection** (card must exist in the main database first):
```
POST /users/ash/cards?tcg=yugioh&card_id=46986414
```

**Search a user's collection:**
```
GET /users/ash/cards?tcg=yugioh&card_name=Dark Magician
```

---

## Data Storage

All data is persisted locally in `session.json` in the project root.

---

## Pages

| Route | Description |
|-------|-------------|
| `/` | Home page |
| `/gallery` | Card gallery |
| `/about` | About page |
| `/contact` | Contact page |
