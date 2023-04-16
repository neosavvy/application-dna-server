import os

from supabase import create_client, Client

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder


from dna.common.data_access.profile_operations import save_or_update_profile
from dna.common.schemas import ProfileUpdate


from dna.tasks.external_tasks import show_message, update_profile_task

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


@app.put("/profiles/{profile_id}")
async def update_profile(profile_id: str, profile: ProfileUpdate):
    # Get the profile with the specified ID from the database
    db_profile = save_or_update_profile(profile, profile_id)

    # Return the updated profile
    return db_profile


@app.put("/profiles/async/{profile_id}")
async def update_profile_async(profile_id: str, profile: ProfileUpdate):
    # Get the profile with the specified ID from the database
    update_profile_task.delay(profile_id, jsonable_encoder(profile))
    # Return the updated profile
    return {"message": "Profile is being updated asynchronously"}
