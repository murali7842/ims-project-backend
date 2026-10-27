import os
import uvicorn
from src.app.config.setting import setting


if __name__ == "__main__":
    port = int(os.getenv("PORT", setting.PORT))
    host = os.getenv("HOST", setting.HOST)
    reload = os.getenv("ENVIRONMENT", "development").lower() == "development"
    uvicorn.run(
        "src.app.app:app",
        host=host,
        port=port,
        reload=reload
    )
