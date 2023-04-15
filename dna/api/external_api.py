from fastapi import FastAPI

from dna.tasks.external_tasks import show_message

app = FastAPI()

profiles = []


@app.get("/health")
async def health():
    return {"message": "I'm alive."}


@app.get("/profiles")
async def get_profiles():

    show_message.delay("Hello, World!")

    return profiles


@app.post("/profiles")
async def create_profile(profile: dict):

    show_message.delay("Hello, World!")

    profiles.append(profile)
    return {"message": "Profile created successfully"}
