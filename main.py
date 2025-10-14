from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from features.membership.application.errors.membership_errors import BaseException
from features.membership.application.errors.membership_errors import handle_exception
from features.membership.settings import create_container
from features.membership.routes import router


app = FastAPI(title="Membership Management API")

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(BaseException, handle_exception)

container = create_container()
app.container = container
