import os

from supabase import create_client, Client

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from datetime import datetime

from dna.common.model import Profile
from dna.common.model.session_management import managed_session
from dna.common.schemas import ProfileUpdate


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


@app.put("/profiles/{profile_id}")
def update_profile(profile_id: str, profile: ProfileUpdate):
    # Get the profile with the specified ID from the database
    db_profile = save_or_update_profile(profile, profile_id)

    # Return the updated profile
    return db_profile


@managed_session
def save_or_update_profile(profile, profile_id, session=None):
    db_profile = session.query(Profile).filter(Profile.id == profile_id).first()
    # If the profile doesn't exist, return a 404 response
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Update the profile with the new values
    if profile.username is not None:
        db_profile.username = profile.username
    if profile.full_name is not None:
        db_profile.full_name = profile.full_name
    if profile.avatar_url is not None:
        db_profile.avatar_url = profile.avatar_url
    if profile.website is not None:
        db_profile.website = profile.website
    db_profile.update_at = datetime.now()

    # Commit the changes to the database
    session.commit()
    return db_profile
