# Python-eveorm

Python-eveorm is a ORM client for [Eve servers](http://python-eve.org/)

## Usage

Python-eveorm is designed to be handled like traditional ORM. Access to resources, find
items or create new items it's done hidding HTTP usage. 

To access on items published by one resource of one Eve Api 

```python
>>> import eveorm
>>> api = eveorm.Api("http://localhost:5002/v1/")
>>> api.resources.users.all()
[<Item users 52b21f56b621471140a921df>, <Item users 52b21fdfb621471140a921e0>]
```

... or create new users and udpate or delete them is easy as well:

```python
>>> user = api.resources.users.new()
>>> user.name = "foo"
>>> user.email = "foo@gmail.com"
>>> user.save()
>>> print user.id
52b21f56b621471140a921df
>>> user.name = "bar"
>>> user.save()
>>> user.delete()
>>> api.resources.users.all()
[]

```

## Install

```
$ git clone https://github.com/pfreixes/python-eveorm
$ cd pyton-eveorm
$ python setup.py install
```

## Run Tests

```
$ unit2 discover -v
test_delete_item (eveorm.tests.test_eveorm.EveOrmTest) ... ok
test_get_all_items (eveorm.tests.test_eveorm.EveOrmTest) ... ok
test_get_resources (eveorm.tests.test_eveorm.EveOrmTest) ... ok
test_new_item (eveorm.tests.test_eveorm.EveOrmTest) ... ok
test_update_item (eveorm.tests.test_eveorm.EveOrmTest) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.374s

OK
```

## Other

Thanks to [Oriol Rius](https://github.com/oriolrius) for fund this project, Standing on the shoulders of giants
