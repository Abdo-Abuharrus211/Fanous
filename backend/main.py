from fastapi import FastAPI

from driver import Driver

app = FastAPI()

# TODO: get the session ID from the frontend???
# Example session_id, replace with actual logic to generate or retrieve it
DRIVER = Driver(session_id="12345")

@app.get("/")
def hello():
    return("Welcome to Fanous' backend. Now, kindly, leave : )")


@app.post("/caption")
async def caption():
    """
    Process the image using and generate a new caption for it.
    """
    payload = await request.get_json()
    DRIVER.process(payload)

def main():
    print("Bob")

if __name__ == "__main__":
    main()
