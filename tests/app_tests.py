import unittest
import starlette.status as sc
from starlette.testclient import TestClient
from app.main import app
from app.models import ChuckNorrisFactDb

client: TestClient = TestClient(app)


class AppTests(unittest.TestCase):

    def test_get_fact(self):
        fact_id = 1
        response = client.get(f'/fact/{fact_id}')
        self.assertEqual(response.status_code, sc.HTTP_200_OK)
        cnf: ChuckNorrisFactDb = ChuckNorrisFactDb.parse_obj(response.json())
        self.assertEqual(cnf.id, fact_id)
        self.assertEqual(cnf.fact, "Google, c'est le seul endroit où tu peux taper Chuck Norris...")

    def test_get_fact_not_found(self):
        fact_id = 11
        response = client.get(f'/fact/{fact_id}')
        self.assertEqual(response.status_code, sc.HTTP_404_NOT_FOUND)

    def test_get_all_facts(self):
        response = client.get('/facts/')
        self.assertEqual(response.status_code, sc.HTTP_200_OK)
        facts = [ChuckNorrisFactDb.parse_obj(fact) for fact in response.json()]
        self.assertEqual(len(facts), 10)
