import os
from supabase import create_client, Client
from fastapi import FastAPI
from dna.tasks.external_tasks import show_message

####
# TODO: Refactor this such that it uses our configuration
####
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
print(f"URL: {url}")
print(f"KEY: {key}")
supabase: Client = create_client(url, key)

app = FastAPI()

profiles = []


@app.get("/health")
async def health():
    return {"message": "I'm alive."}


@app.get("/profiles")
async def get_profiles():

    show_message.delay("Hello, World!")

    response = supabase\
        .table('profiles')\
        .select("*")\
        .eq('name', 'Adam')\
        .execute()

    print(f"Response: {response}")

    return response


@app.post("/profiles")
async def create_profile(profile: dict):

    show_message.delay("Hello, World!")

    profiles.append(profile)
    return {"message": "Profile created successfully"}
