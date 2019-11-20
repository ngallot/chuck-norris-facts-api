from typing import Optional, Tuple, List, Dict
from app.logging_utils import build_logger
from app import config

logger = build_logger(logger_name=__name__, config=config.logging_config)

"""Fake database to simulate calls to a real database. Here, database composed of a dictionary of id -> value"""
_DB: Dict[int, str] = {
    0: "Chuck Norris a déjà compté jusqu'à l'infini. Deux fois.",
    1: "Google, c'est le seul endroit où tu peux taper Chuck Norris...",
    2: "Certaines personnes portent un pyjama Superman. Superman porte un pyjama Chuck Norris.",
    3: "Chuck Norris donne fréquemment du sang à la Croix-Rouge. Mais jamais le sien.",
    4: "Chuck Norris et Superman ont fait un bras de fer, le perdant devait mettre son slip par dessus son pantalon.",
    5: "Chuck norris se souvient très bien de son futur",
    6: "Peter Parker a été mordu par une araignée, Clark Kent a été mordu par Chuck Norris",
    7: "Chuck Norris peut écrire un traitement de texte avec la souris.",
    8: "Chuck Norris peut faire des ronds avec une equerre",
    9: "La seule chose qui arrive à la cheville de Chuck Norris... c'est sa chaussette."
}


class ObjectNotFoundError(Exception):
    pass


def next_id() -> int:
    return max(_DB.keys()) + 1


def get_facts(ids: Optional[List[int]] = None) -> Optional[List[Tuple[int, str]]]:
    facts = [(k, v) for k, v in _DB.items()] if not ids else [(id, get_fact(fact_id=id)) for id in ids]
    return [f for f in facts if f[1]] if facts else None


def get_fact(fact_id: int) -> Optional[str]:
    return _DB.get(fact_id, None)


def insert_fact(fact: str) -> Tuple[int, str]:
    try:
        id = next_id()
        _DB[id] = fact
        return id, fact
    except Exception as e:
        logger.error(f'Error while inserting fact {fact}: {e}')
        raise e


def update_fact(fact_id: int, new_fact: str) -> None:
    fact = get_fact(fact_id)
    if not fact:
        raise ObjectNotFoundError(f'Fact with id {fact_id} does not exist')
    else:
        _DB[fact_id] = new_fact


def delete_fact(fact_id: int) -> None:
    fact = get_fact(fact_id)
    if not fact:
        raise ObjectNotFoundError(f'Fact with id {fact_id} does not exist')
    else:
        _DB.pop(fact_id)

