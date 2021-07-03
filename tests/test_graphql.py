import pytest
import graphene
from graphene.test import Client
from blbook.schema import  Query, UserType


@pytest.mark.django_db
def test_all_users():
    schema = graphene.Schema(query=Query)
    client = Client(schema)
    executed = client.execute('''{allUsers {id}}''')
    assert executed['data'] 