# Fanous Backend

This service processes the images for Fanous.

Using computer-vision to analysze, describe, and generate the short names.

# Tech Stack

1. FastAPI: simple, _fast_, HTTP framework to get up and running quickly and efficiently.
2. Moondream2: a highly efficient vision model that's great and identifying and describing features in complex images.
   Runs on edge, needing only 2 GB of RAM to run on non-GPU nodes.

# Local Dev

To run the project, using the `uv` package manager: `uv run fastapi dev`
or better yet `uv run uvicorn main:app --reload --port 8001`

# Settings and Configuration

The app is configured via `config.py` which inherits from `pydantic.BaseSettings` and loads environment variables
automatically, including from `.env` file. The project includes a `.env.example` file with the required environment
variables and their default values.
## Environment values resolution:
**Values precedence:** env var > .env file > class default
 Example:
1. Constructor arguments: Settings(debug=True) overrides everything 
2. Environment variables: FANOUS_DEBUG=true in the shell 
3. `.env` file: values in FANOUS_DEBUG=true inside `.env`
4. Class defaults: debug: bool = False in the class definition

//TODO: Add more to README

# License
