from fastapi import FastAPI, UploadFile, File, HTTPException

from driver import Driver

app = FastAPI()

# TODO: get the session ID from the frontend???
# Example session_id, replace with actual logic to generate or retrieve it
DRIVER = Driver(session_id="12345")

@app.get("/")
def hello():
    return {"message": "Welcome to Fanous' backend. Now, kindly, leave : )"}


@app.post("/caption")
async def caption(image: UploadFile = File(...)):
    """
    Process the image and generate a caption and descriptive name.

    API Contract:
    POST /caption
      Content-Type: multipart/form-data
      Body: image (file)
    Response: { "name": "descriptive_name", "description": "full caption" }
    """
    contents = await image.read()
    filename = image.filename
    # pass the contents to the driver so model can infer
    processed = await DRIVER.process(contents)

    if not processed or processed is None:
        raise HTTPException(status_code=500, detail="Captioning process failed")

    return {"name": processed["name"], "description": processed["description"]}
