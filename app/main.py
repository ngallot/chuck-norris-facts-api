from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app.logging_utils import build_logger
from app import __version__, config

logger = build_logger(logger_name=__name__, config=config.logging_config)
app = FastAPI(
    title=config.app_config.name,
    description=config.app_config.description,
    debug=config.app_config.debug,
    version=__version__
)

logger.info(f'{config.app_config.name} server started successfully.')


@app.get('/', description='API homepage')
def root():
    return RedirectResponse(url='/docs')

