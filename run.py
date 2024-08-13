import logging
import os
import io

import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware

from src.api.api import router
from src.models.base import Base
from src.db.base import engine
from src.core.config import settings
from src.services.caching import SharedCaching
from src.services.resource_manager import ResourceManager

import subprocess

# Logger
logging.config.fileConfig(settings.LOGGING_CONFIG_FILE, disable_existing_loggers=False)

# Init SQLite database
Base.metadata.create_all(bind=engine)

def prepare_data_dir() -> None:
    try:
        # Create data_dir
        os.makedirs(os.path(settings.DATA_DIR))

        # Create resource folder
        os.makedirs(os.path.join(settings.DATA_DIR, 'resources'))

        # Create database
        db_path = os.path.join(settings.DATA_DIR, 't2parser.db')
        if not os.path.isfile(db_path):
            with io.open(db_path, 'w') as file:
                pass
    except Exception:
        return

def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url="/docs",
        redoc_url='/re-docs',
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        description='T2 Parser'
    )
    
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL)
    application.include_router(router, prefix=settings.API_PREFIX)

    return application


if __name__ == '__main__':
    # Init data dir
    prepare_data_dir()

    # Init Resource Manager instance
    ResourceManager.Instance().path = os.path.join(settings.DATA_DIR, 'resources')

    gui_cmd = ['streamlit', 'run', './src/gui/gui.py']
    process = subprocess.Popen(gui_cmd)

    app = get_application()
    uvicorn.run(app, host="0.0.0.0", port=8090)
