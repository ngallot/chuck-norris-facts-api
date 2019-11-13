from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app import __version__, config

app = FastAPI(
    title=config.app_config.name,
    description=config.app_config.description,
    debug=config.app_config.debug,
    version=__version__
)


@app.get('/', description='API homepage')
def root():
    return RedirectResponse(url='/docs')

