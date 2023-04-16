from datetime import datetime

from fastapi import HTTPException

from dna.common.model import Profile
from dna.common.model.session_management import managed_session


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
