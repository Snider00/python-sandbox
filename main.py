from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import uvicorn  
import random

first = random.randint(1, 1000000000)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    regen = random.randint(1, 1000000000)
    return templates.TemplateResponse("index.html", {"request": request, "name": "Welcome", "color": "green", "regen": regen, "first": first})
@app.get("/gallery")
def home(request: Request):
    return templates.TemplateResponse("gallery.html", {"request": request, "color": "green",})
@app.get("/about")
def home(request: Request):
    return templates.TemplateResponse("about.html", {"request": request, "color": "green",})
@app.get("/contact")
def home(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request, "email": "snider@snider.com", "color": "green",})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)