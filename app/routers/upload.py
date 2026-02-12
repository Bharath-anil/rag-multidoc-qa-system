from fastapi import APIRouter,UploadFile

router =APIRouter()

@router.get("/health")
def health_check():
    return {"status":"Healthy"}


@router.post("/upload")
def upload_doc(file:UploadFile):
    return { "message": "File received" }