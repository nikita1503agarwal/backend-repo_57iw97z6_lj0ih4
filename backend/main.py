from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import ChildProfile

app = FastAPI(title="EcoKids API", version="0.1.0")

# CORS for local dev + sandbox previews
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProfileCreate(BaseModel):
    nickname: str
    age_group: str
    parent_email: EmailStr


@app.get("/test")
async def test():
    ok = db is not None
    return {"ok": ok}


@app.post("/profiles")
async def create_profile(payload: ProfileCreate):
    profile = ChildProfile(
        nickname=payload.nickname,
        age_group=payload.age_group,
        parent_email=str(payload.parent_email),
        eco_points=0,
    )
    inserted_id = create_document("childprofile", profile)
    return {"id": inserted_id, **profile.model_dump()}


@app.get("/profiles")
async def list_profiles(parent_email: Optional[EmailStr] = Query(None)):
    query = {}
    if parent_email:
        query["parent_email"] = str(parent_email)
    docs = get_documents("childprofile", query)

    def serialize(doc):
        doc["id"] = str(doc.get("_id"))
        doc.pop("_id", None)
        # Convert datetime to ISO for safety
        if "created_at" in doc:
            doc["created_at"] = doc["created_at"].isoformat() if hasattr(doc["created_at"], "isoformat") else doc["created_at"]
        if "updated_at" in doc:
            doc["updated_at"] = doc["updated_at"].isoformat() if hasattr(doc["updated_at"], "isoformat") else doc["updated_at"]
        return doc

    return [serialize(d) for d in docs]
