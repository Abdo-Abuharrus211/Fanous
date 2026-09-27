from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return("Welcome to Fanous' backend. Now, kindly, leave : )")


@app.post("/caption")
async def caption():
    """
    Process the image using and generate a new caption for it.
    """
    pass


def main():
    print("Bob")

if name__ == "__main__":
    main()
