import json
import requests

from datetime import datetime
import hashlib
import base64


class AmberAPIError(object):

    def __init__(self, status_code, body):
        self.body = body
        self.status_code = status_code

def _send_request(url, public_key, private_key, method='GET',
                 data=None, headers=None):
    if not data:
        data = {}
    if not headers:
        headers = {'Content-Type': 'application/json'}
    timestamp = datetime.isoformat(datetime.utcnow())
    request_data = {
        'url': url,
        'data': data,
        'headers': headers,
        'timestamp': timestamp,
        'api_key': public_key
    }
    request_string = json.dumps(request_data, sort_keys=True)
    request_data['signature'] = base64.b64encode(hashlib.sha256(
        request_string + private_key).hexdigest())
    r = False
    if method == 'GET':
        r = requests.get(url, data=json.dumps(request_data), headers=headers)
    elif method == 'PUT':
        r = requests.put(url, data=json.dumps(request_data), headers=headers)
    elif method == 'POST':
        r = requests.post(url, data=json.dumps(request_data), headers=headers)
    elif method == 'DELETE':
        r = requests.delete(url, data=json.dumps(request_data), headers=headers)

    if r and r.status_code == 200:
        return json.loads(r.text)
    raise AmberAPIError(r.status_code, json.loads(r.text))

class AmberAPI(object):

    def init(self, api_url, pub_key, pri_key):
        self.api_url = api_url
        self.pub_key = pub_key
        self.pri_key = pri_key

    def _url(self, *path):
        return self.api_url + "/api/v1/" + "/".join([str(x) for x in path])

    def _get(self, *path, **data):
        url = self._url(*path)
        headers = {'Content-Type': 'application/json'}
        args = {
            'url': url,
            'public_key': self.pub_key,
            'private_key': self.pri_key,
            'method': 'GET',
            'data': json.dumps(data),
            'headers': headers
        }
        return _send_request(**args)

    def _post(self, *path, **data):
        url = self._url(*path)
        headers = {'Content-Type': 'application/json'}
        if 'data_list' in data:
            data = data['data_list']
        args = {
            'url': url,
            'public_key': self.pub_key,
            'private_key': self.pri_key,
            'method': 'POST',
            'data': json.dumps(data),
            'headers': headers
        }
        return _send_request(**args)

    def _post_list(self, data_list, *path):
        url = self._url(*path)
        headers = {'Content-Type': 'application/json'}
        args = {
            'url': url,
            'public_key': self.pub_key,
            'private_key': self.pri_key,
            'method': 'POST',
            'data': json.dumps(data_list),
            'headers': headers
        }
        return _send_request(**args)

    def _put(self, *path, **data):
        url = self._url(*path)
        headers = {'Content-Type': 'application/json'}
        args = {
            'url': url,
            'public_key': self.pub_key,
            'private_key': self.pri_key,
            'method': 'PUT',
            'data': json.dumps(data),
            'headers': headers
        }
        return _send_request(**args)

    def _delete(self, *path):
        url = self._url(*path)
        headers = {'Content-Type': 'application/json'}
        args = {
            'url': url,
            'public_key': self.pub_key,
            'private_key': self.pri_key,
            'method': 'DELETE',
            'data': json.dumps(None),
            'headers': headers
        }
        return _send_request(**args)


    def _search(self, *path, **data):
        url = self._url(*path)
        headers = {'Content-Type': 'application/json'}
        args = {
            'url': url,
            'public_key': self.pub_key,
            'private_key': self.pri_key,
            'method': 'POST',
            'data': json.dumps(data),
            'headers': headers
        }
        return _send_request(**args)

    # PRODUCT:

    def get_product(self, prod_id):
        return self._get('products', prod_id)

    def get_products(self, params):
        return self._get('products', **params)

    def search_products(self, params):
        return self._search('products', 'search', **params)

    def add_product(self, data):
        return self._post('products', **data)

    def update_product(self, prod_id, data):
        return self._put('products', prod_id, **data)

    def delete_product(self, prod_id):
        return self._delete('products', prod_id)

    # IMAGES:

    def get_images(self, prod_id):
        return self._get('products', prod_id, 'images')

    def add_image(self, prod_id, data):
        return self._post('products', prod_id, 'images', **data)

    def get_image(self, prod_id, img_id):
        return self._get('products', prod_id, 'images', img_id)

    def edit_image(self, prod_id, img_id, data):
        return self._put('products', prod_id, 'images', img_id, **data)

    def delete_image(self, prod_id, img_id):
        return self._delete('products', prod_id, 'images', img_id)

    # OPTIONS:

    def get_options(self, prod_id):
        return self._get('products', prod_id, 'options')

    def add_option(self, prod_id, data):
        return self._post('products', prod_id, 'options', **data)

    def get_option(self, prod_id, opt_id):
        return self._get('products', prod_id, 'options', opt_id)

    def edit_option(self, prod_id, opt_id, data):
        return self._put('products', prod_id, 'options', opt_id, **data)

    def delete_option(self, prod_id, opt_id):
        return self._delete('products', prod_id, 'options', opt_id)

    # TAGS:

    def get_tags(self, prod_id):
        return self._get('products', prod_id, 'tags')

    def delete_tag(self, prod_id, tag_id):
        return self._delete('products', prod_id, 'tags', tag_id)

    def add_tags(self, prod_id, new_tags):
        return self._post_list(new_tags, 'products', prod_id, 'tags')

    # MANUFACTURER:

    def get_manufacturer(self, mfr_id):
        return self._get('manufacturers', mfr_id)

    def get_manufacturers(self):
        return self._get('manufacturers')

    # USER:

    def get_roles(self):
        return self._get('role')

    def get_user(self, user_id):
        return self._get('users', user_id)

    def get_users(self):
        return self._get('users')

    def add_user(self, data):
        return self._post('users', **data)

    def update_user(self, user_id, data):
        return self._put('users', user_id, **data)

    def delete_user(self, user_id):
        return self._delete('users', user_id)

    # COLLECTIONS:

    def get_collections(self):
        return self._get('collections')
