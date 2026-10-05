from fastapi import FastAPI, UploadFile, File, HTTPException

from driver import Driver

app = FastAPI()

DRIVER = Driver()


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
    processed = await DRIVER.process_with_tokenizer(contents)

    if not processed:
        raise HTTPException(status_code=500, detail="Captioning process failed")

    return {"name": processed["name"], "description": processed["description"]}
