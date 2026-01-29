from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn  
import random
import requests

first = random.randint(1, 1000000000)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

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
@app.get('/get_website')
def get_website():
    response = requests.get('https://www.tcgplayer.com/product/554977/yugioh-battles-of-legend-terminal-revenge-dragon-master-magia-quarter-century-secret-rare?page=1&Language=English&utm_campaign=20486200459&utm_source=google&utm_medium=cpc&utm_content=703416088519&utm_term=&adgroupid=161217872788&gad_source=1&gad_campaignid=20486200459&gclid=Cj0KCQiAp-zLBhDkARIsABcYc6u_oywdr4UV9ZP_ci3Pc0fkygd0lc159bfBVE3VPlmaqcvA_w3OspYaAgjlEALw_wcB')
    return HTMLResponse(
        content=response.text,
        status_code=200,
        headers={}
    )
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)