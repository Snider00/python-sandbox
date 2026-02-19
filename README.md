# 📚 TCG Card Collection API  

A lightweight **FastAPI** service for storing, searching, and managing trading‑card game (TCG) cards and user collections.  
All data is persisted in a simple JSON file (`session.json`) – no external database required.

---

<details>
<summary>🔧 Table of Contents</summary>

1. [Overview](#overview)  
2. [Prerequisites](#prerequisites)  
3. [Installation](#installation)  
4. [Running the Server](#running-the-server)  
5. [API Endpoints](#api-endpoints)  
6. [Project Structure](#project-structure)  
7. [Testing the API](#testing-the-api)  
8. [Contributing](#contributing)  
9. [License](#license)  

</details>

---

## Overview  

- **FastAPI** based HTTP API  
- Stores cards per TCG (e.g., *Yu‑Gi‑Oh*, *Magic: The Gathering*)  
- Supports global card pool **and** per‑user collections  
- Simple JSON persistence (`session.json`) – ideal for prototypes or small projects  
- HTML pages (`index.html`, `gallery.html`, …) served via Jinja2 templates  

---

## Prerequisites  

| Tool | Minimum Version |
|------|-----------------|
| Python | **3.9** |
| pip   | latest |
| uvicorn (ASGI server) | installed via `pip` |

---

## Installation  

```bash
# 1️⃣ Clone the repository
git clone https://github.com/your‑username/tcg‑card‑api.git
cd tcg-card-api

# 2️⃣ Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate

# 3️⃣ Install dependencies
pip install -r requirements.txt
```

`requirements.txt` contains:

```
fastapi
uvicorn[standard]
pydantic
jinja2
requests
```

---

## Running the Server  

```bash
# Start the app (default host 127.0.0.1, port 8000)
python main.py
```

The API will be reachable at **http://127.0.0.1:8000**.  
OpenAPI docs are automatically generated at **/docs** and **/redoc**.

---

## API Endpoints  

| Method | Path | Description | Example |
|--------|------|-------------|---------|
| `GET` | `/` | Home page (rendered HTML) | `http://localhost:8000/` |
| `GET` | `/gallery` | Gallery page | `http://localhost:8000/gallery` |
| `GET` | `/about` | About page | `http://localhost:8000/about` |
| `GET` | `/contact` | Contact page (email shown) | `http://localhost:8000/contact` |
| `GET` | `/add?a=&b=` | Simple addition (demo) | `http://localhost:8000/add?a=3&b=5` |
| `GET` | `/get_website` | Proxy a remote TCG page (HTML) | `http://localhost:8000/get_website` |
| `POST` | `/add_cards` | Add a card to the **global** pool | See body example below |
| `GET` | `/search_cards` | Search global cards (filters: `tcg`, `card_name`, `card_id`) | `http://localhost:8000/search_cards?tcg=YuGiOh` |
| `DELETE` | `/delete_cards` | Delete a global card | `?tcg=YuGiOh&card_id=123` |
| `POST` | `/users/{username}` | Create a new user | `POST /users/alice` |
| `GET` | `/users` | List all users | `GET /users` |
| `POST` | `/users/{username}/cards` | Add a card to a **user** collection | See body example below |
| `GET` | `/users/{username}/cards` | Search a user’s cards | `GET /users/alice/cards?tcg=YuGiOh` |
| `DELETE` | `/users/{username}/cards` | Delete a user’s card | `?tcg=YuGiOh&card_id=123` |

### Request Body for `POST /add_cards` & `POST /users/{username}/cards`

```json
{
  "tcg": "YuGiOh",
  "card_id": "554977",
  "card_name": "Dragon Master Magia",
  "image": "https://example.com/image.png"   // optional
}
```

All responses are JSON (or HTML for the template routes).

---

## Project Structure  

```
tcg-card-api/
├─ main.py               # FastAPI app (the code you posted)
├─ session.json          # Persistent storage (auto‑created)
├─ requirements.txt
├─ templates/
│   ├─ index.html
│   ├─ gallery.html
│   ├─ about.html
│   └─ contact.html
└─ README.md             # ← This file
```

- **main.py** – contains all route definitions and helper functions.  
- **session.json** – JSON object where cards and users are stored.  
- **templates/** – Jinja2 HTML templates used by the GET routes.

---

## Testing the API  

You can use **cURL**, **HTTPie**, or any REST client (Postman, VS Code REST Client).

```bash
# Add a card globally
http POST http://localhost:8000/add_cards \
    tcg=YuGiOh \
    card_id=554977 \
    card_name="Dragon Master Magia"

# List all cards for a TCG
http GET "http://localhost:8000/search_cards?tcg=YuGiOh"

# Create a user
http POST http://localhost:8000/users/alice

# Add a card to Alice's collection
http POST http://localhost:8000/users/alice/cards \
    tcg=YuGiOh \
    card_id=123456 \
    card_name="Blue-Eyes White Dragon"
```

---

## Contributing  

1. Fork the repo.  
2. Create a feature branch: `git checkout -b feature/awesome-feature`.  
3. Commit your changes and push to your fork.  
4. Open a Pull Request – describe the changes and reference any relevant issues.

Please keep the code style consistent (PEP 8) and update the documentation when adding new endpoints.

---

## License  

This project is licensed under the **MIT License** – see the `LICENSE` file for details.  --- 

*Happy coding!* 🚀
