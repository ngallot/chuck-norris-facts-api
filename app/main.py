from typing import List, Optional
from fastapi import FastAPI, Query, HTTPException
from starlette.responses import RedirectResponse
import starlette.status as sc
from app.logging_utils import build_logger
import app.db as db
from app import models
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


@app.get('/facts/', description='Retrieve Chuck Norris facts from the database. Optional filter on the ids to '
                                'retrieve.', response_model=List[models.ChuckNorrisFactDb])
def get_facts(ids: List[int] = Query(
    default=None, title='ids', description='The list of ids to retrieve')) -> List[models.ChuckNorrisFactDb]:
    chuck_norris_fact_db = lambda id, fact: models.ChuckNorrisFactDb.parse_obj(dict(id=id, fact=fact))
    try:
        if ids:
            facts = [(id, db.get_fact(fact_id=id)) for id in ids]
            return [chuck_norris_fact_db(id=id, fact=fact) for (id, fact) in facts if fact is not None]
        else:
            return [chuck_norris_fact_db(id, fact) for (id, fact) in db.get_all_facts()]
    except db.ObjectNotFoundError as err:
        raise HTTPException(status_code=sc.HTTP_404_NOT_FOUND, detail=str(err))
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=sc.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


