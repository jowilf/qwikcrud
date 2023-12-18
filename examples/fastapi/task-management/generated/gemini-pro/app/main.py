from app.admin import init_admin
from app.endpoints import project, task, user
from app.pre_start import init
from app.settings import settings
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from libcloud.storage.types import ObjectDoesNotExistError
from sqlalchemy_file.exceptions import ValidationError as FileValidationError
from sqlalchemy_file.storage import StorageManager


def create_app():
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        on_startup=[init],
    )

    _app.include_router(user.router, prefix="/api/v1/users")
    _app.include_router(project.router, prefix="/api/v1/projects")
    _app.include_router(task.router, prefix="/api/v1/tasks")
    _app.mount("/static", StaticFiles(directory="static"), name="static")
    init_admin(_app)

    return _app


templates = Jinja2Templates(directory="templates")

app = create_app()


@app.get("/", include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "settings": settings}
    )


@app.get("/medias", response_class=FileResponse, tags=["medias"])
async def serve_files(path: str):
    try:
        file = StorageManager.get_file(path)
        return FileResponse(
            file.get_cdn_url(), media_type=file.content_type, filename=file.filename
        )
    except ObjectDoesNotExistError:
        return JSONResponse({"detail": "Not found"}, status_code=404)


@app.exception_handler(FileValidationError)
async def sqla_file_validation_error(request: Request, exc: FileValidationError):
    return JSONResponse({"error": {"key": exc.key, "msg": exc.msg}}, status_code=422)
