from fastapi import APIRouter, UploadFile, File, HTTPException
from services.face_service import get_face_encoding, recognize_face

router = APIRouter()

@router.post("/encode")
async def encode_face(file: UploadFile = File(...)):
    try:
        encoding = await get_face_encoding(file)
        return {"encoding": encoding}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recognize")
async def recognize(file: UploadFile = File(...)):
    try:
        result = await recognize_face(file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
