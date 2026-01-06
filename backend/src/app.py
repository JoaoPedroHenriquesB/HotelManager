from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.routers.room_router import rm_router
from src.utils.exceptions import NotFoundError, PermissionDeniedError, InternalDomainError, DuplicateEntityError


app = FastAPI(title="Hotel Manager")
app.include_router(rm_router)

@app.get("/")
def health()-> dict:
  return {"message": "healthy"}


# --- ERROR HANDLER ---
@app.exception_handler(NotFoundError)
async def not_found_exception_handler(request: Request, exc: NotFoundError):
  return JSONResponse(status_code=404, content={"message": "requested item not found"})

@app.exception_handler(PermissionDeniedError)
async def permission_denied_handler(request: Request, exc: PermissionDeniedError):
    return JSONResponse(status_code=403, content={"message": "you are not allowed to perform this action."})

@app.exception_handler(DuplicateEntityError)
async def duplicated_entity_error_handler(request: Request, exc: PermissionDeniedError):
    return JSONResponse(status_code=409, content={"message": "a record with this data already exists in the database."})

@app.exception_handler(InternalDomainError)
async def internal_error_handler(request: Request, exc: InternalDomainError):
    return JSONResponse(status_code=500,content={"message": "internal server error ocurred."})
# --- ERROR HANDLER ---
