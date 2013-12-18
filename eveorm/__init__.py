
"""
    python-eveorm
    ~~~~~~~~~~~~~

    A python orm client for Eve servers

    :copyright: (c) 2011 by Pau Freixes.
    :license: BSD, see LICENSE for more details.

    Quick guide
    ~~~~~~~~~~~~~

    Access to items of one resource published by one Eve Api

    >>> import eveorm
    >>> api = eveorm.Api("http://localhost:5002/v1/")
    >>> api.resources.users.all()
    [<Item users 52b21f56b621471140a921df>, <Item users 52b21fdfb621471140a921e0>]
    >>> user = api.resources.users.all()[1]
    >>> user.name
    "user name"

    Create, update or delete items

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
"""

__title__ = 'python-eveorm'
__version__ = '0.1'
__author__ = 'Pau Freixes'
__license__ = 'BSD'
__copyright__ = 'Copyright 2013 Pau Freixes'

from eveorm.api import Api
from eveorm.api import Resource
from eveorm.api import Item
