import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.app.common.exception.exception_handler import register_exception
from src.app.config.db_config import init_models
from src.app.config.setting import get_setting
from src.app.routers.auth_router import authRouter
from src.app.routers.batch_router import batch_router
from src.app.routers.course_router import course_router
from src.app.routers.dashboard_router import dashboard_router
from src.app.routers.institution_router import institution_router
from src.app.routers.operator_router import operator_router
from src.app.routers.payment_router import payment_router
from src.app.routers.student_assessment_router import student_assessment_router
from src.app.routers.student_router import student_router
from src.app.routers.teacher_router import teacher_router
from src.app.routers.user_router import user_router

setting = get_setting()
log = logging.getLogger()


@asynccontextmanager
async def register_init(app: FastAPI):
    log.info(setting.DATABASE_URL)
    await init_models()
    print("Sample")
    yield


def register_app():
    # FastAPI
    app = FastAPI(
        title=setting.TITLE,
        version=setting.VERSION,
        description=setting.DESCRIPTION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        swagger_ui_default_parameters={"displayRequestDuration": True},
        lifespan=register_init
    )

    # register_static_file(app)

    register_middleware(app)

    register_router(app)

    # register_page(app)

    register_exception(app)

    return app


def register_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def register_router(app: FastAPI):

    app.include_router(
        institution_router,
        prefix=f"{setting.API_V1_PREFIX}/institution",
        tags=["Institution"]
    )
    app.include_router(
        user_router,
        prefix=f"{setting.API_V1_PREFIX}/user",
        tags=["User"]
    )
    app.include_router(
        authRouter,
        prefix=f"{setting.API_V1_PREFIX}/auth",
        tags=["Authentication"]
    )
    app.include_router(
        operator_router,
        prefix=f"{setting.API_V1_PREFIX}/operator",
        tags=["Operator"]
    )
    app.include_router(
        teacher_router,
        prefix=f"{setting.API_V1_PREFIX}/teacher",
        tags=["Teacher"]
    )
    app.include_router(
        course_router,
        prefix=f"{setting.API_V1_PREFIX}/course",
        tags=["Course"]
    )
    app.include_router(
        batch_router,
        prefix=f"{setting.API_V1_PREFIX}/batch",
        tags=["Batch"]
    )
    app.include_router(
        student_router,
        prefix=f"{setting.API_V1_PREFIX}/student",
        tags=["Student"]
    )
    app.include_router(
        payment_router,
        prefix=f"{setting.API_V1_PREFIX}/payment",
        tags=["Payment"]
    )
    app.include_router(
        student_assessment_router,
        prefix=f"{setting.API_V1_PREFIX}/student_assessment",
        tags=["StudentAssessment"]
    )
    app.include_router(
        dashboard_router,
        prefix=f"{setting.API_V1_PREFIX}/dashboard",
        tags=["Dashboard"]
    )






