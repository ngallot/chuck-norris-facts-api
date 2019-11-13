from pydantic import BaseModel, Schema


class ChuckNorrisFactBase(BaseModel):
    fact: str = Schema(default=..., title='fact', description='The Chuck Norris Fact')


class ChuckNorrisFactDb(ChuckNorrisFactBase):
    id: int = Schema(default=..., title='id', description='The database id of the Chuck Norris Fact')

