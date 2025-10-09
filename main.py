from fastapi import FastAPI

from features.membership.settings import create_container
from features.membership.routes import router


app = FastAPI(title="Membership Management API")

app.include_router(router)

container = create_container()
app.container = container
