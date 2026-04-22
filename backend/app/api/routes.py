from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse

from app.logging_system.logging_utils import setup_logging
from app.services.plagiarism_service import run_plagiarism_pipeline


router = APIRouter()
logger = setup_logging()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/compare-files")
async def compare_files(files: list[UploadFile] = File(...)):
    if not files:
        return JSONResponse({"error": "No files uploaded."}, status_code=400)

    file_pairs = []
    for upload in files:
        name = upload.filename or "document.txt"
        if not name.lower().endswith(".txt"):
            return JSONResponse(
                {"error": f"Only .txt files are supported (got: {name})."},
                status_code=400,
            )

        raw = await upload.read()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            return JSONResponse(
                {"error": f"File could not be read as UTF-8: {name}"},
                status_code=400,
            )
        file_pairs.append((name, text))

    logger.info("Running compare-files for %s document(s).", len(file_pairs))
    result = run_plagiarism_pipeline(file_pairs)
    if "error" in result:
        return JSONResponse(result, status_code=400)
    return result


@router.post("/compare-against-collection")
async def compare_against_collection(files: list[UploadFile] = File(...)):
    return await compare_files(files)
