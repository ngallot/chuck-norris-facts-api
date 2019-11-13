from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app import __version__

app = FastAPI(
    title='Chuck Norris Facts API',
    description='A RESTful API exposing Chuck Norris facts',
    debug=True,
    version=__version__
)

@app.get('/', description='API homepage')
def root():
    return RedirectResponse(url='/docs')

