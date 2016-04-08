#Embedded file name: /Users/curtislagraff/.virtualenvs/amber-lib/amber-lib/benchmarking/search.py


class NewCached(object):

    def __init__(self):
        self._name = 'new API, locally cached'

    def setup(self):
        import amber_lib
        import amber_lib.filter as filter

        class Context(object):
            public = '4dc5aec0bdbac2fe1acdeccd00d8b883532306b1be64b48f7f94000f2ab1fd2f'
            private = '6c8d1089133a0a1f11922ce9009be0d3198835fc0592671bac1453634f1ab137'
            host = 'http://127.0.0.1'
            port = '8080'
            request_attempts = 3
            cache = 'system=redis;host=localhost;port=6379;db=5'

        self.conn = amber_lib.Connection(Context())
        self.data = filter.Predicate('IdentityComponent.product_name', filter.equal('blah'))

    def test(self):
        self.conn.Product.query(filtering=self.data)


class New(object):

    def __init__(self):
        self._name = 'new API'

    def setup(self):
        import amber_lib
        import amber_lib.filter as filter

        class Context(object):
            public = '4dc5aec0bdbac2fe1acdeccd00d8b883532306b1be64b48f7f94000f2ab1fd2f'
            private = '6c8d1089133a0a1f11922ce9009be0d3198835fc0592671bac1453634f1ab137'
            host = 'http://127.0.0.1'
            port = '8080'
            request_attempts = 3
            cache = ''

        self.conn = amber_lib.Connection(Context())
        self.data = filter.Predicate('IdentityComponent.product_name', filter.equal('blah'))

    def test(self):
        self.conn.Product.query(filtering=self.data)


class Old(object):

    def __init__(self):
        self._name = 'old'

    def setup(self):
        import amber_lib
        self.amber_client = amber_lib.AmberClient('http://localhost:8001', '4dc5aec0bdbac2fe1acdeccd00d8b883532306b1be64b48f7f94000f2ab1fd2f', '6c8d1089133a0a1f11922ce9009be0d3198835fc0592671bac1453634f1ab137')
        self.data = {u'category': u'',
         u'terms': u'blah',
         u'sort_key': u'',
         u'selected': [],
         u'limit': 100,
         u'offset': 0,
         u'sort_direction': u'',
         u'return_ids': True}

    def test(self):
        self.amber_client.search_products(self.data)
