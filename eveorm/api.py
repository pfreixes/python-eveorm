# -*- coding: utf-8 -*-
import requests
import json

class RequestException(Exception):
    def __init__(self, url, action, status_code, msg=None):
        self.action = action
        self.url = url
        self.status_code = status_code
        self.msg = msg

    def __repr__(self):
        msg = "RequestException explained\n"+\
              "  URL: %s %s\n" % (self.action, self.url) +\
              "  HTTP ERROR: %s\n" % self.status_code +\
              "  RESPONSE MSG: %s\n" % self.msg +\
              "--------------------------\n"
        return msg
    def __str__(self):
        msg = "RequestException explained\n"+\
              "  URL: %s %s\n" % (self.action, self.url) +\
              "  HTTP ERROR: %s\n" % self.status_code +\
              "  RESPONSE MSG: %s\n" % self.msg +\
              "--------------------------\n"

        return msg

class Request:
    _global_headers = {}

    cache_control = False

    @classmethod
    def global_headers(cls, headers):
        Request._global_headers = headers

    @classmethod
    def get(cls, url, json=True, headers=None, params=None):
        if not headers:
            headers = {}

        if Request.cache_control is False:
            headers["Cache-Control"] = "no-cache"

        if Request._global_headers:
            headers.update(Request._global_headers)

        r = requests.get(url, headers=headers, params=params)
        if r.status_code != 200:
            raise RequestException(url, "GET", r.status_code, r.text)

        if json:
            return r.json()
        else:
            return r.text

    @classmethod
    def post(cls, url, payload, json=True, headers=None):
        if not headers:
            headers = {}

        if Request.cache_control is False:
            headers["Cache-Control"] = "no-cache"

        if Request._global_headers:
            headers.update(Request._global_headers)

        r = requests.post(url, data=payload, headers=headers)
        if r.status_code != 200:
            raise RequestException(url, "POST", r.status_code, r.text)

        if json:
            return r.json()
        else:
            return r.text
      
    @classmethod
    def patch(cls, url, payload, json=True, headers=None):
        if not headers:
            headers = {}

        if Request.cache_control is False:
            headers["Cache-Control"] = "no-cache"

        if Request._global_headers:
            headers.update(Request._global_headers)

        r = requests.patch(url, data=payload, headers=headers)
        if r.status_code != 200:
            raise RequestException(url, "PATCH", r.status_code, r.text)
        if json:
            return r.json()
        else:
            return r.text

    @classmethod
    def delete(cls, url, json=True, headers=None):
        if not headers:
            headers = {}

        if Request.cache_control is False:
            headers["Cache-Control"] = "no-cache"

        if Request._global_headers:
            headers.update(Request._global_headers)

        r = requests.delete(url, headers=headers)
        if r.status_code != 200:
            raise RequestException(url, "DELETE", r.status_code, r.text)
        if json:
            return r.json()
        else:
            return r.text

        
class ContentNotReadable(Exception):
    pass

class ContentNotWritable(Exception):
    pass


class Item:
    """
    Items is a register belonging at one resource, it is typed using `Resource.new` function or
    using a classmethod `Item.copy` where you can choose the destination type of one Item.

    >>> city = api.resource.cities.new()
    >>> print city.type
    cities

    Fields are created like attributes, all atributes that they does not begin with "_" character
    are get how attribures:

    >>> city = api.resources.cities.new()
    >>> city.name = "barcelona"
    >>> city.asdfasdf = "be carefull it will be get how attriburte"
    >>> city.save()
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "agh/syncdb/eveorm.py", line 322, in save
      raise ContentNotWritable(response)
      eveorm.ContentNotWritable: {u'item': {u'status': u'ERR', u'issues': [u"unknown field 'asdfasdf'"]}}
    """
    class _Field:
        _field_name = "field_%s"
        def __init__(self, value, name):
            self.value = value
            self.name = name

        @staticmethod
        def name(name):
            return Item._Field._field_name % name

    _internal_fields = ["_id", "etag", "_links",
                        "updated", "created"]

    def __init__(self, resource, name, fields = {}, force_new_id=None, force_new_updated=None, force_new_created=None):
        """
        Init a new Item belong at one resource 
        """
        self._resource = resource
        self._name = name
        self._force_id = force_new_id
        self._force_updated = force_new_updated
        self._force_created = force_new_created
        self._id = None
        self._etag = None
        self._url = None
        self._updated = None
        self._created = None
 
        if fields:
            for name, value in fields.items():
                if name not in Item._internal_fields:
                    setattr(self, name, value)

            if "_id" in fields:
                self._id = fields["_id"]
            if "etag" in fields:
                self._etag = fields["etag"]
            if "updated" in fields:
                self._updated = fields["updated"]
            if "created" in fields:
                self._created = fields["created"]

            try:
                self._url = self._resource._schema + fields["_links"]["self"]["href"]
            except KeyError:
                self._url = None
 
          
    @classmethod
    def copy(cls, resource, item, keep_id=True, keep_updated=True, keep_created=True):
        """
        Return a new Item that it is a copy of item instance for another
        resource. Use keep_id to keep the id between items
        """
        if keep_id:
            force_new_id = item.id
        else:
            force_new_id = None

        if keep_updated:
            force_new_updated = item.updated
        else:
            force_new_updated = None

        if keep_created:
            force_new_created = item.created
        else:
            force_new_created = None

        return Item(resource, resource.name,
                    fields=item.fields(), force_new_id=force_new_id,
                    force_new_updated=force_new_updated, force_new_created=force_new_created)

    def __setattr__(self, name, value):
        if name.find("_") > -1:
            self.__dict__[name] = value
        else:
            self.__dict__[Item._Field.name(name)] = Item._Field(value, name)

    def __getattr__(self, name):
        try:
            field = self.__dict__[Item._Field.name(name)]
        except KeyError:
            raise AttributeError()
        return field.value

    def __repr__(self):
        return "<Item %s %s>" % (self._name, self._id)

    def __eq__(self, b):
        if self._id or b._id:
            return self._id == b._id
        else:
            return False 

    @property
    def id(self):
        return self._id

    @property
    def url(self):
        return self._url

    @property
    def type(self):
        return self._name

    def save(self):
        if self._id is None:
            # create payload
            fields = self.fields()
            if self._force_updated is not None:
                fields["updated"] = self._force_updated
            if self._force_created is not None:
                fields["created"] = self._force_created
            if self._force_id:
                fields["_id"] = self._force_id

            payload = "item=%s" % (json.dumps(fields))
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            try:
                response = Request.post(self._resource.url, payload, headers=headers)
            except Exception, e:
                raise e

            if "item" in response and response["item"]["status"] == "OK":
                self._updated = response["item"]["updated"]
                self._id = response["item"]["_id"]
                self._url = self._resource._schema +  response["item"]["_links"]["self"]["href"]
                self._etag = response["item"]["etag"]
                if self._force_created is not None:
                    self._created = self._force_created
            else:
                raise ContentNotWritable(response)
        else:
            fields = self.fields()
            if self._force_updated is not None:
                fields["updated"] = self._force_updated
            if self._force_created is not None:
                fields["created"] = self._force_created

            payload = "item=%s" % (json.dumps(fields))
            headers = {"If-Match": self._etag,
                       "Content-Type": "application/x-www-form-urlencoded"}
            try:
                response = Request.patch(self.url, payload, headers=headers)
            except Exception, e:
                raise e

            if "item" in response and response["item"]["status"] == "OK":
                self._updated = response["item"]["updated"]
                #self._created = response["item"]["created"]
                self._id = response["item"]["_id"]
                self._url = self._resource._schema +  response["item"]["_links"]["self"]["href"]
                self._etag = response["item"]["etag"]

                if self._force_created is not None:
                    self._created = self._force_created
            else:
                raise ContentNotWritable(response)

    def delete(self):
        if not self._id:
           raise ContentNotWritable("Id param missed")
        if not self._etag:
           raise ContentNotWritable("etag param missed")
        if not self._url:
           raise ContentNotWritable("url param missed")

        headers = {"If-Match": self._etag}
        try:
            response = Request.delete(self.url, headers=headers)
        except Exception, e:
            raise e


    def update(self, fields, updated=None, created=None):
        """
        Update all item fields with new values set at fields
        dictionary
        """
        for name, value in fields.items():
            if name not in Item._internal_fields:
                setattr(self, name, value)

        if updated:
            self._force_updated = updated
        if created:
            self._force_created = created

    def fields(self):
        """
        Return a dictionary with all fields of this item
        """
        d = {}
        for k, v  in self.__dict__.items():
            if isinstance(v, Item._Field):
                d[v.name] = v.value
        return d

    @property
    def updated(self):
        return self._updated

    @property
    def created(self):
        return self._created

    @property
    def etag(self):
        return self._etag


class Resource:
    """
    Resource object implements the object to speak with resources
    published by one Eve server, with :class:`Collection` instance 
    you can acces to all resources published by it.

    Otherwise you can get direct accces if you know the url to
    handle it and the name of the resource

        >>> from eveorm import Resource
        >>> r = Resource("http://localhost:5000/v1/users", "users")
        >>> user = r.all()[0]
        >>> same_user = r.get(user.id)
        >>> assert(user == same_user)
    """

    def __init__(self, url, name):
        self.name = name
        self.url = url
        self._schema = "http://"

    def get(self, id):
        """
        Return one item that it belongs at this resource
        """
        j = Request.get(self.url + "/" + id)
        return Item(self, self.name, fields=j)

    def all(self):
        """
        Return all items for this resource
        """
        return self._query(self.url)
 
    def find(self, filter_dict):
        """
        Return items that them gets filter dictionary conditional query

        >>> api.resources.users.find({"where": "name=='foo'"})
        """
        return self._query(self.url, params=filter_dict)
 
    def _query(self, url, params=None):
        items = []
        while url:
            j = Request.get(url, params=params)
            if j is None:
                raise NotReadable()
       
            if "_items" in j:
                for item in j["_items"]:
                    items.append(Item(self, self.name, fields=item))

            if "next" in j["_links"]:
                url = "http://" + j["_links"]["next"]["href"]
            else:
                url = None
        return items

    def new(self):
        """
        Return one empty Item for this resource.
        """
        return Item(self, self.name)


class Api:
    """
    The Api object implements the  main object need to
    acces over al resources - aka collections - published by one
    Eve Server.

    Usually you create a :class:`Colllection` to get acces over
    one Eve service, like this:

        >>> from eveorm import Api
        >>> api = Api("http://localhost:5000/v1/")
    """

    def __init__(self, url):
        self.url = url
        self._schema = "http://"
        self._resources = {}
        
        # get and parse eve endpoint
        j = Request.get(self.url, json=True)

        if "_links" not in j:
            raise ContentNotReadable("_links unavailable")

        if "child" not in  j["_links"]:
            raise ContentNotReadable("child unavailable")

        for resource in j["_links"]["child"]:
            name = resource["title"]
            url = self._schema + resource["href"]
            self._resources[name] = Resource(url, name)

    @property
    def resources(self):
        class _get_resource:
            def __init__(self, resources):
                self._resources = resources

            def __getattr__(self, key):
                if key not in self._resources:
                    raise AttributeError()
                return self._resources[key]

        return _get_resource(self._resources)


if __name__ == "__main__":
    # minimal test
    try:
        import datetime
        now = datetime.datetime.now().replace(tzinfo=None)
        now = now - datetime.timedelta(0, 3600)
        print now.strftime("%Y-%m-%dT%H:%M:%SZ")
        api = Api("http://localhost:5001/v1")
        users = api.resources.users
        l = users.all()
        user = users.get(l[0].id)
        assert(user == l[0])
        user.email = "kk"
        user.save()
        print user.updated
        new_user = users.new()
        new_user.name = "hola"
        new_user.email = "pajaro"
        new_user.save()
        print user.updated
        users_find = users.find({"where": "name==\"hola\""})
        assert(len(users_find) > 1)
        updated_users = users.find({"where": "updated>=date(\"%s\")" % now.strftime("%Y-%m-%dT%H:%M:%S")})
        print updated_users
        assert(len(updated_users) == 2)
        user.delete()
    except RequestException, e:
        import sys
        print e
        print sys.exc_info()
