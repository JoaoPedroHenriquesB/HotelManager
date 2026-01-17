from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.utils.exceptions import (
  CouldNotValidateCredentialsError,
  DuplicateEntityError,
  GuestNotFoundError,
  InternalDomainError,
  NotActiveStayError,
  NotAdminError,
  NotFoundError,
  PermissionDeniedError,
  RoomNotAvaliableError,
  RoomNotFoundError,
  StayNotFoundError,
  TokenDecodeError,
  TokenExpiredSignatureError,
)


# --- ERRORS HANDLER ---
def setup_exceptions(app: FastAPI):


  @app.exception_handler(NotFoundError)
  async def not_found_exception_handler(request: Request, exc: NotFoundError):
      return JSONResponse(
          status_code=404, content={"message": "requested item not found"})


  @app.exception_handler(RoomNotFoundError)
  async def room_not_found_error(request: Request, exc: NotFoundError):
      return JSONResponse(status_code=404, content={"message": "room not found"})


  @app.exception_handler(StayNotFoundError)
  async def stay_not_found_error(request: Request, exc: NotFoundError):
      return JSONResponse(status_code=404, content={"message": "stay not found"})


  @app.exception_handler(GuestNotFoundError)
  async def guest_not_found_error(request: Request, exc: NotFoundError):
      return JSONResponse(status_code=404, content={"message": "guest not found."})


  @app.exception_handler(RoomNotAvaliableError)
  async def room_not_avaliable_error(request: Request, exc: RoomNotAvaliableError):
      return JSONResponse(
          status_code=404, content={"message": "the room requested is already occupied."})


  @app.exception_handler(PermissionDeniedError)
  async def permission_denied_handler(request: Request, exc: PermissionDeniedError):
      return JSONResponse(
          status_code=403,
          content={"message": "you are not allowed to perform this action."})


  @app.exception_handler(DuplicateEntityError)
  async def duplicated_entity_error_handler(request: Request, exc: PermissionDeniedError):
      return JSONResponse(
          status_code=409,
          content={"message": "duplicate entity."})


  @app.exception_handler(InternalDomainError)
  async def internal_error_handler(request: Request, exc: InternalDomainError):
      return JSONResponse(
          status_code=500, content={"message": "internal server error occurred."})


  @app.exception_handler(CouldNotValidateCredentialsError)
  async def could_not_validate_credentials_error_handler(request: Request, exc: CouldNotValidateCredentialsError):
      return JSONResponse(
          status_code=401,
          content={"message": "could not validate credentials"})


  @app.exception_handler(TokenExpiredSignatureError)
  async def token_expired_signature_error_handler(request: Request, exc: TokenExpiredSignatureError):
      return JSONResponse(
          status_code=401,
          content={"message": "token expired"})


  @app.exception_handler(NotAdminError)
  async def not_admin_error_handler(request: Request, exc: NotAdminError):
      return JSONResponse(
          status_code=403,
          content={"message": "you are not an admin"})


  @app.exception_handler(TokenDecodeError)
  async def token_decode_error_handler(request: Request, exc: TokenDecodeError):
      return JSONResponse(
          status_code=401,
          content={"message": "token decode error"})


  @app.exception_handler(NotActiveStayError)
  async def not_active_stay_error_handler(request: Request, exc: NotActiveStayError):
      return JSONResponse(
          status_code=403,
          content={"message": "stay is not active"})
