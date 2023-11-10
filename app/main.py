import os
import coloredlogs, logging
from http.client import HTTPConnection
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from app.prisma import prisma
from app.api import api
from app.middleware.jwt_auth import BearerAuthBackend
from app.middleware.custom_auth import auth_middleware

### Loggin config
logging.config.fileConfig('app/logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)
log_level = os.getenv("LOG_LEVEL",None)
coloredlogs.install(fmt='%(levelname)-0s: %(asctime)s,%(msecs)03d | hostname=%(hostname)s | logger=%(name)s[proc=%(process)d] | message=%(message)s  | call_trace=%(pathname)s at line %(lineno)s in func %(funcName)s()',level=log_level , logger=logger, isatty=True)

HTTPConnection.debuglevel = 1
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

app = FastAPI()

# app.middleware("http")(auth_middleware)


app.add_middleware(AuthenticationMiddleware, backend=BearerAuthBackend())

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(api, prefix="/api")


@app.on_event("startup")
async def startup():
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()


@app.get("/")
def read_root():
    return {"Hello": "Notification"}
