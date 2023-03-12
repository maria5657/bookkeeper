from bookkeeper.repository.sqlite_repository import SQLiteRepository
from inspect import get_annotations

from dataclasses import dataclass

import pytest

@dataclass(slots=True)
class Custom():
    comment: str = 'Hi!'
    name: str = 'Marcus Aurelius'
    one: int = 1
    test: str = ''
    pk: int | None = None
    

@pytest.fixture
def repo():
    return SQLiteRepository('TEST_REPO_DONT_USE.db', Custom)

def test_crud(repo):
    repo.delete_all()
    obj1 = Custom('Hello', pk = 1)
    pk1 = repo.add(obj1)
    obj2 = Custom('Hi', pk = 2)
    pk2 = repo.add(obj2)
    assert obj1 == repo.get(pk1) # saves correctly
    assert obj2 == repo.get(pk2) # saves correctly
    assert obj1 != repo.get(pk2) # different keys
    assert obj2 != repo.get(pk1) # really different keys
    obj_buff = obj1
    obj2.pk = obj1.pk
    repo.update(obj2)
    assert repo.get(pk1) != obj_buff # the recording really changed
    assert repo.get(pk1) == obj2 # changed for the new version
    repo.delete(pk2)
    assert repo.get(pk2) is None

def test_cannot_delete_unexistent(repo):
    with pytest.raises(KeyError):
        repo.delete(1000)

def test_cannot_update_without_pk(repo):
    obj = Custom()
    print(obj)
    with pytest.raises(TypeError):
        repo.update(obj)

def test_get_all(repo):
    data_size = 5 
    repo.delete_all()
    objects = [Custom(pk = i+1) for i in range(data_size)]
    for o in objects:
        repo.add(o)
    all = repo.get_all()
    for i in range(data_size):
        assert all[i] == objects[i]

def test_get_all_with_condition(repo):
    data_size = 5
    repo.delete_all()
    objects = []
    for i in range(data_size):
        o = Custom(pk = i+1)
        o.name = str(i)
        o.test = 'test'
        repo.add(o)
        objects.append(o)
    assert repo.get_all({'name': '0'})[0] == objects[0]
    all = repo.get_all({'test': 'test'})
    for i in range(data_size):
        assert all[i] == objects[i]
