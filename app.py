from fastapi import FastAPI, Request, HTTPException, Form
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from youtube_api import search_channels_by_niche
from chart_generator import generate_chart
from utils import validate_niche_input

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/result", response_class=HTMLResponse)
async def result(request: Request, niche: str = Form(...)):
    try:
        validate_niche_input(niche)

        # Fetch channel data and create DataFrame
        df = search_channels_by_niche(niche, max_results=15)

        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "niche": niche,
                "df": df.to_dict(orient='records')  # Convert DataFrame to dictionary for rendering
            },
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate_chart", response_class=HTMLResponse)
async def generate_chart_route(request: Request, niche: str = Form(...), chart_type: str = Form(...)):
    try:
        validate_niche_input(niche)

        # Fetch channel data and create DataFrame
        df = search_channels_by_niche(niche, max_results=15)

        # Generate chart
        chart_path = generate_chart(df.to_dict(orient='records'), chart_type)

        return templates.TemplateResponse(
            "chart.html",
            {
                "request": request,
                "niche": niche,
                "chart_path": f"/static/{chart_path}",
            },
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)