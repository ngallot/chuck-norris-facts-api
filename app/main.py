from typing import List, Optional, Union, Tuple
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


@app.get('/fact/{fact_id}', description='Retrieve a Chuck Norris fact from its id',
         response_model=models.ChuckNorrisFactDb, tags=['Facts'])
def get_fact(fact_id: int) -> models.ChuckNorrisFactDb:
    try:
        fact = db.get_fact(fact_id=fact_id)
    except db.ObjectNotFoundError as e:
        raise HTTPException(
            status_code=sc.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=sc.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Error while retrieving fact with id {fact_id}: {e}'
        )
    if fact:
        return models.ChuckNorrisFactDb(id=fact_id, fact=fact)
    else:
        raise HTTPException(
            status_code=sc.HTTP_404_NOT_FOUND,
            detail=f'Fact with id {fact_id} not found.'
        )


@app.get('/facts/', description='Retrieve Chuck Norris facts from the database. Optional filter on the ids to '
                                'retrieve.', response_model=List[models.ChuckNorrisFactDb], tags=['Facts'])
def get_facts(ids: List[int] = Query(
    default=None, title='ids', description='The list of ids to retrieve')) -> List[models.ChuckNorrisFactDb]:
    try:
        facts: Optional[List[Tuple[int, str]]] = db.get_facts(ids=ids)
    except db.ObjectNotFoundError as err:
        raise HTTPException(status_code=sc.HTTP_404_NOT_FOUND, detail=str(err))
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=sc.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    chuck_norris_fact_db = lambda id, fact: models.ChuckNorrisFactDb(id=id, fact=fact)
    if facts:
        return [chuck_norris_fact_db(id=id, fact=fact) for (id, fact) in facts]
    else:
        raise HTTPException(status_code=sc.HTTP_404_NOT_FOUND,
                            detail=f'Facts with ids {",".join(map(str, ids))} not found')


