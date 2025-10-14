from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class BaseException(Exception):
    status_code: int
    message: str


class ErrorResponse(BaseModel):
    status_code: int
    message: str


class MembershipNotFoundError(BaseException):
    def __init__(self, membership_id: str):
        self.status_code = status.HTTP_404_NOT_FOUND
        self.message = f"Membership with id '{membership_id}' not found"


class MembershipAlreadyExistsError(BaseException):
    def __init__(self, membership_id: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = f"Membership with id '{membership_id}' already exists"


class MembershipAlreadyExistsByNameError(BaseException):
    def __init__(self, membership_name: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = f"Membership with name '{membership_name}' already exists"


class MembershipInUseError(BaseException):
    def __init__(self, membership_id: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = f"Membership with id '{membership_id}' is in use"


class DailyMembershipExistsError(BaseException):
    def __init__(self, gym_id: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.message = f"Daily membership already exists for gym '{gym_id}'"


async def handle_exception(request, error: BaseException):
    return JSONResponse(
        status_code=error.status_code,
        content=ErrorResponse(
            status_code=error.status.value,
            message=error.message,
        ).model_dump(),
    )
