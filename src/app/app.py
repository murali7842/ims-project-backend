from fastapi import FastAPI
from src.app.config.register import register_app

app = register_app()

# app = FastAPI(
#     default_response_class=ORJSONResponse,
#     docs_url=setting.DOCS_URL,
#     redoc_url=setting.REDOC_URL,
#     root_path="/api",
#     lifespan=lifespan,
#     swagger_ui_default_parameters={"displayRequestDuration": True},
#     title=setting.APP_NAME,
#     version=setting.VERSION,
#     description=setting.DESCRIPTION,
# )

@app.get("/")
def root():
    return {"message": "Service Running"}