from fastapi import APIRouter
from app.db.mongo import (
    summaries_collection,
    plagiarism_collection,
    autocorrect_collection
)

router = APIRouter(prefix="/history", tags=["History"])


@router.get("/")
def get_history():
    summaries = list(summaries_collection.find({}, {"_id": 0}).sort("created_at", -1).limit(10))
    plagiarism = list(plagiarism_collection.find({}, {"_id": 0}).sort("created_at", -1).limit(10))
    autocorrect = list(autocorrect_collection.find({}, {"_id": 0}).sort("created_at", -1).limit(10))

    return {
        "summaries": summaries,
        "plagiarism": plagiarism,
        "autocorrect": autocorrect
    }