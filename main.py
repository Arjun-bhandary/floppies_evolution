from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import Response
import tempfile
from agent import Agent  # make sure file is named agent.py

app = FastAPI()

@app.post("/evolve-pet")
async def evolve_pet(image: UploadFile = File(...), art_style: str = Form("")):
    # Save uploaded image temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(await image.read())
        tmp_path = tmp.name

    # Call Agent to evolve image (returns raw bytes)
    evolved_img_bytes = Agent.evolve(tmp_path, art_style)

    # Return PNG directly
    return Response(content=evolved_img_bytes, media_type="image/png")
