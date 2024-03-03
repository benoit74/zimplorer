import sys
from asyncio import Task
from contextlib import asynccontextmanager
from http import HTTPStatus
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request

from zimplorer import __about__
from zimplorer.constants import BackendConf, logger
from zimplorer.routes import dummy

PREFIX = "/v1"


class Main:
    def __init__(self) -> None:
        self.background_tasks = set[Task[Any]]()

    @asynccontextmanager
    async def lifespan(self, _: FastAPI):
        # Startup
        if BackendConf.processing_enabled:
            logger.info("Starting processing")
        else:
            logger.warning("Processing is disabled")
        # Startup complete
        yield
        # Shutdown

    def task_stopped(self, task_name: str, task: Task[Any]) -> None:
        if task.cancelled():
            return
        exc = task.exception()
        self.background_tasks.discard(task)
        if exc:
            logger.error(f"{task_name} has stopped anormally", exc_info=exc)
            sys.exit(1)

    def create_app(self) -> FastAPI:
        self.app = FastAPI(
            title=__about__.__api_title__,
            description=__about__.__api_description__,
            version=__about__.__version__,
            lifespan=self.lifespan,
        )

        @self.app.get("/api")
        async def landing() -> RedirectResponse:  # pyright: ignore
            """Redirect to root of latest version of the API"""
            return RedirectResponse(
                f"/api/{__about__.__api_version__}/",
                status_code=HTTPStatus.TEMPORARY_REDIRECT,
            )

        api = FastAPI(
            title=__about__.__api_title__,
            description=__about__.__api_description__,
            version=__about__.__version__,
            docs_url="/",
            openapi_tags=[
                {
                    "name": "all",
                    "description": "all APIs",
                },
            ],
            contact={
                "name": "Benoit74",
                "url": "---",
                "email": "---",
            },
            license_info={
                "name": "GNU General Public License v3.0",
                "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
            },
        )

        api.add_middleware(
            CORSMiddleware,
            allow_origins=BackendConf.allowed_origins,
            allow_credentials=False,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        api.include_router(router=dummy.router)

        self.app.mount(f"/api/{__about__.__api_version__}", api)

        class ServeVueUiFromRoot(BaseHTTPMiddleware):
            """Custom middleware to serve the Vue.JS application

            We need a bit of black magic to:
            - serve the Vue.JS UI from "/"
            - but still keep the API on "/api"
            - and support Vue.JS routes like "/home"
            - and still return 404 when the UI is requesting a file which does not exits
            """

            ui_location = Path()

            async def dispatch(
                self, request: Request, call_next: RequestResponseEndpoint
            ):
                path = request.url.path

                # API is served normally
                if path.startswith("/api"):
                    response = await call_next(request)
                    return response

                # Serve index.html on root
                if path == "/":
                    return FileResponse(BackendConf.ui_location.joinpath("index.html"))

                local_path = BackendConf.ui_location.joinpath(path[1:])

                # If there is no dot, then we are probably serving a Vue.JS internal
                # route, so let's serve Vue.JS app
                if "." not in local_path.name:
                    return FileResponse(BackendConf.ui_location.joinpath("index.html"))

                # If the path exists and is a file, serve it
                if local_path.exists() and local_path.is_file():
                    return FileResponse(local_path)

                # Otherwise continue to next handler (which is probably a 404)
                response = await call_next(request)
                return response

        # Apply the custom middleware
        self.app.add_middleware(ServeVueUiFromRoot)

        return self.app
