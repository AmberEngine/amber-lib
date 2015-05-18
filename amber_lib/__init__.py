import json
import requests

from datetime import datetime
import hashlib
import base64
import decimal


class ObjectEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return str(obj)

        return super(ObjectEncoder, self).default(obj)


class AmberError(Exception):

    def __init__(self, status_code, body):
        self.body = body
        self.status_code = status_code
        Exception.__init__(self, body)


def _send_request(
    url,
    public_key,
    private_key,
    method='GET',
    data=None,
    headers=None
):
    retries = 3
    r = False
    while retries > 0:
        if not data:
            data = {}
        if not headers:
            headers = {'Content-Type': 'application/amber+json'}
        timestamp = datetime.isoformat(datetime.utcnow())
        request_data = {
            'url': url,
            'data': data,
            'headers': headers,
            'timestamp': timestamp,
            'public_key': public_key
        }
        request_string = json.dumps(
            request_data,
            sort_keys=True,
            cls=ObjectEncoder
        )
        request_data['signature'] = base64.b64encode(hashlib.sha256(
            request_string + private_key).hexdigest())
        r = False
        if method == 'GET':
            r = requests.get(
                url,
                data=json.dumps(request_data, cls=ObjectEncoder),
                headers=headers
            )
        elif method == 'PUT':
            r = requests.put(
                url,
                data=json.dumps(request_data, cls=ObjectEncoder),
                headers=headers
            )
        elif method == 'POST':
            r = requests.post(
                url,
                data=json.dumps(request_data, cls=ObjectEncoder),
                headers=headers
            )
        elif method == 'DELETE':
            r = requests.delete(
                url,
                data=json.dumps(request_data, cls=ObjectEncoder),
                headers=headers
            )
        if r and r.status_code == 200:
            response = json.loads(r.text)
            response.pop('_documentation', None)
            return response
        else:
            retries -= 1
    try:
        raise AmberError(r.status_code, json.loads(r.text))
    except ValueError:
        raise AmberError(r.status_code, r.text)


class AmberClient(object):
    def __init__(self, api_url, pub_key, pri_key):
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
            'data': json.dumps(data, cls=ObjectEncoder),
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
            'data': json.dumps(data, cls=ObjectEncoder),
            'headers': headers
        }
        return _send_request(**args)

    def _post_list(
            self,
            data_list,
            *path
    ):
        url = self._url(*path)
        headers = {'Content-Type': 'application/json'}
        args = {
            'url': url,
            'public_key': self.pub_key,
            'private_key': self.pri_key,
            'method': 'POST',
            'data': json.dumps(data_list, cls=ObjectEncoder),
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
            'data': json.dumps(data, cls=ObjectEncoder),
            'headers': headers
        }
        return _send_request(**args)

    def _delete(self, *path, **data):
        url = self._url(*path)
        headers = {'Content-Type': 'application/json'}
        args = {
            'url': url,
            'public_key': self.pub_key,
            'private_key': self.pri_key,
            'method': 'DELETE',
            'data': json.dumps(data, cls=ObjectEncoder),
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
            'data': json.dumps(data, cls=ObjectEncoder),
            'headers': headers
        }
        return _send_request(**args)

    def update_ngram_index(self):
        return self._get(
            'update_ngram_index'
        )

    # PRODUCT:

    def get_product(
            self,
            prod_id,
            data=None
    ):
        if not data:
            data = {}
        return self._get(
            'products',
            prod_id,
            **data
        )

    def get_product_component(
            self,
            prod_id,
            component_name
    ):
        return self._get(
            'products',
            prod_id,
            'components',
            component_name
        )

    def get_products(
            self,
            params
    ):
        return self._get(
            'products',
            **params
        )

    def search_products(
            self,
            params
    ):
        return self._search(
            'products',
            'search',
            **params
        )

    def add_product(
            self,
            data
    ):
        return self._post(
            'products',
            **data
        )

    def update_product(
            self,
            prod_id,
            data
    ):
        return self._put(
            'products',
            prod_id,
            **data
        )

    def update_product_component(
            self,
            prod_id,
            component_name,
            data
    ):
        return self._put(
            'products',
            prod_id,
            'components',
            component_name,
            **data
        )

    def get_product_sub_component(
            self,
            prod_id,
            component_name,
            sub_component_data_id
    ):
        return self._get(
            'products',
            prod_id,
            'sub_components',
            component_name,
            sub_component_data_id,
        )

    def add_product_option_set(
            self,
            prod_id,
            data
    ):
        return self._post(
            'products',
            prod_id,
            'options',
            **data
        )

    def remove_product_option_set(
            self,
            prod_id,
            option_set_id
    ):
        return self._delete(
            'products',
            prod_id,
            'options',
            option_set_id
        )

    def add_product_sub_component(
            self,
            prod_id,
            component_name,
            data
    ):
        return self._post(
            'products',
            prod_id,
            'sub_components',
            component_name,
            **data
        )

    def update_product_sub_component(
            self,
            prod_id,
            component_name,
            sub_component_data_id,
            data
    ):
        return self._put(
            'products',
            prod_id,
            'sub_components',
            component_name,
            sub_component_data_id,
            **data
        )

    def delete_product_sub_component(
            self,
            prod_id,
            component_name,
            sub_component_data_id
    ):
        return self._delete(
            'products',
            prod_id,
            'sub_components',
            component_name,
            sub_component_data_id
        )

    def delete_product(
            self,
            prod_id
    ):
        return self._delete(
            'products',
            prod_id
        )

    def delete_products(
            self,
            data
    ):
        return self._delete(
            'products',
            **data
        )

    def get_product_listing(
            self,
            params
    ):
        return self._get(
            'product_listing',
            **params
        )

    # IMAGES:

    def get_images(
            self,
            prod_id
    ):
        response = self._get(
            'products',
            prod_id,
            'images'
        )
        return response.get('images', [])

    def add_image(
            self,
            prod_id,
            data
    ):
        return self._post(
            'products',
            prod_id,
            'images',
            **data
        )

    def get_image(
            self,
            img_id
    ):
        return self._get(
            'images',
            img_id
        )

    def edit_image(
            self,
            img_id,
            data
    ):
        return self._put(
            'images',
            img_id,
            **data
        )

    def delete_image(
            self,
            img_id
    ):
        return self._delete(
            'images',
            img_id
        )

    # MANUFACTURER IMAGES:

    def get_manufacturer_images(
            self,
            mfr_id
    ):
        response = self._get(
            'manufacturers',
            mfr_id,
            'manufacturer_images'
        )
        return response.get('manufacturer_images', [])

    def add_manufacturer_image(
            self,
            mfr_id,
            data
    ):
        return self._post(
            'manufacturers',
            mfr_id,
            'manufacturer_images',
            **data
        )

    def get_manufacturer_image(
            self,
            mfr_id,
            mfr_img_id
    ):
        return self._get(
            'manufacturers',
            mfr_id,
            'manufacturer_images',
            mfr_img_id
        )

    def edit_manufacturer_image(
            self,
            mfr_id,
            mfr_img_id,
            data
    ):
        return self._put(
            'manufacturers',
            mfr_id,
            'manufacturer_images',
            mfr_img_id,
            **data
        )

    def delete_manufacturer_image(
            self,
            mfr_id,
            mfr_img_id
    ):
        return self._delete(
            'manufacturers',
            mfr_id,
            'manufacturer_images',
            mfr_img_id
        )

    def search_manufacturers(
            self,
            params
    ):
        response = self._search(
            'manufacturers',
            'search',
            **params
        )
        return response.get('manufacturers', [])

    # OPTION SETS:

    def get_option_sets(
            self,
            manufacturer_id
    ):
        response = self._get(
            'manufacturers',
            manufacturer_id,
            'option_sets'
        )
        return response.get('option_sets', [])

    def add_option_set(
            self,
            manufacturer_id,
            data
    ):
        return self._post(
            'option_sets',
            manufacturer_id,
            **data
        )

    def get_option_set(
            self,
            option_set_id
    ):
        return self._get(
            'option_sets',
            option_set_id
        )

    def edit_option_set(
            self,
            option_set_id,
            data
    ):
        return self._put(
            'option_sets',
            option_set_id,
            **data
        )

    def delete_option_set(
            self,
            option_set_id
    ):
        return self._delete(
            'option_sets',
            option_set_id
        )

    # OPTIONS:

    def get_options(
            self,
            option_set_id
    ):
        response = self._get(
            'option_sets',
            option_set_id,
            'options'
        )
        return response.get('options', [])

    def add_option(
            self,
            option_set_id,
            data
    ):
        return self._post(
            'option_sets',
            option_set_id,
            'options',
            **data
        )

    def get_option(
            self,
            option_id
    ):
        return self._get(
            'options',
            option_id
        )

    def edit_option(
            self,
            option_id,
            data
    ):
        return self._put(
            'options',
            option_id,
            **data
        )

    def delete_option(
            self,
            option_id
    ):
        return self._delete(
            'options',
            option_id
        )

    # TAGS:

    def get_tags(
            self,
            prod_id
    ):
        response = self._get(
            'products',
            prod_id,
            'tags'
        )
        return response.get('tags', [])

    def delete_tag(
            self,
            prod_id,
            tag_id
    ):
        return self._delete(
            'products',
            prod_id,
            'tags',
            tag_id
        )

    def add_tags(
            self,
            prod_id,
            new_tags
    ):
        return self._post_list(
            new_tags,
            'products',
            prod_id,
            'tags'
        )

    # MANUFACTURER:

    def get_manufacturer(
            self,
            mfr_id
    ):
        return self._get(
            'manufacturers',
            mfr_id
        )

    def get_manufacturers(
            self,
            data
    ):
        response = self._get(
            'manufacturers',
            **data
        )
        return response.get('manufacturers', [])

    def add_manufacturer(
            self,
            data
    ):
        return self._post(
            'manufacturers',
            **data
        )

    def update_manufacturer(
            self,
            mfr_id,
            data
    ):
        return self._put(
            'manufacturers',
            mfr_id,
            **data
        )

    # API KEY

    def get_roles(self):
        response = self._get(
            'roles'
        )
        return response.get('roles', [])

    def get_api_key(
            self,
            api_key_id
    ):
        return self._get(
            'api_keys',
            api_key_id
        )

    def get_api_keys(self):
        response = self._get(
            'api_keys'
        )
        return response.get('api_keys', [])

    def add_api_key(
            self,
            data,
    ):
        return self._post(
            'api_keys',
            **data
        )

    def update_api_key(
            self,
            api_key_id,
            data
    ):
        return self._put(
            'api_keys',
            api_key_id,
            **data
        )

    def delete_api_key(
            self,
            api_key_id
    ):
        return self._delete(
            'api_keys',
            api_key_id
        )

    # CLIENT KEY

    def get_client_key(
            self,
            client_key_id
    ):
        return self._get(
            'client_keys',
            client_key_id
        )

    def get_client_keys(self):
        response = self._get(
            'client_keys'
        )
        return response.get('client_keys', [])

    def add_client_key(
            self,
            data
    ):
        return self._post(
            'client_keys',
            **data
        )

    def update_client_key(
            self,
            client_key_id,
            data
    ):
        return self._put(
            'client_keys',
            client_key_id,
            **data
        )

    def delete_client_key(
            self,
            client_key_id
    ):
        return self._delete(
            'client_keys',
            client_key_id
        )

    # USER KEY:

    def get_user_key(
            self,
            user_key_id
    ):
        return self._get(
            'user_keys',
            user_key_id
        )

    def get_user_key_by_public_key(
            self,
            public_key
    ):
        return self._get(
            'user_keys',
            public_key
        )

    def get_user_keys(self):
        response = self._get(
            'user_keys'
        )
        return response.get('user_keys', [])

    def add_user_key(
            self,
            data
    ):
        return self._post(
            'user_keys',
            **data
        )

    def update_user_key(
            self,
            user_key_id,
            data
    ):
        return self._put(
            'user_keys',
            user_key_id,
            **data
        )

    def delete_user_key(
            self,
            user_key_id
    ):
        return self._delete(
            'user_keys',
            user_key_id
        )

    # USER (deprecated):

    def get_user(
            self,
            api_key_id
    ):
        return self._get(
            'api_keys',
            api_key_id
        )

    # SALES CHANNELS:

    def get_sales_channel_preference(
            self,
            mfr_id,
            sc_id
    ):
        return self._get(
            'manufacturers',
            mfr_id,
            'preferences',
            sc_id
        )

    def add_sales_channel_preference(
            self,
            mfr_id,
            sc_id,
            data
    ):
        return self._post(
            'manufacturers',
            mfr_id,
            'preferences',
            sc_id,
            **data
        )

    def update_sales_channel_preference(
            self,
            mfr_id,
            sc_id,
            data
    ):
        return self._put(
            'manufacturers',
            mfr_id,
            'preferences',
            sc_id,
            **data
        )

    def get_sales_channels(
            self,
            data=None
    ):
        if not data:
            data = {}
        response = self._get(
            'sales_channels',
            **data
        )
        return response.get('sales_channels', [])

    def get_sales_channel(
            self,
            sc_id
    ):
        return self._get(
            'sales_channels',
            sc_id
        )

    def add_sales_channel(
            self,
            data
    ):
        return self._post(
            'sales_channels',
            **data
        )

    def update_sales_channel(
            self,
            sc_id,
            data
    ):
        return self._put(
            'sales_channels',
            sc_id,
            **data
        )

    def delete_sales_channel(
            self,
            sc_id
    ):
        return self._delete(
            'sales_channels',
            sc_id
        )

    def sales_channel_get_product(
            self,
            sc_id,
            mfr_id
    ):
        response = self._get(
            'sales_channels',
            sc_id,
            'manufacturers',
            mfr_id,
            'products'
        )
        return response.get('sales_channel_products', [])

    def sales_channel_add_product(
            self,
            sc_id,
            data
    ):
        return self._post(
            'sales_channels',
            sc_id,
            'products',
            **data
        )

    def sales_channel_remove_product(
            self,
            sc_id,
            data
    ):
        return self._delete(
            'sales_channels',
            sc_id,
            'products',
            **data
        )

    def sales_channel_add_manufacturer(
            self,
            sc_id,
            mfr_id,
            data
    ):
        return self._post(
            'sales_channels',
            sc_id,
            'manufacturers',
            mfr_id,
            **data
        )

    def sales_channel_remove_manufacturer(
            self,
            sc_id,
            mfr_id
    ):
        return self._delete(
            'sales_channels',
            sc_id,
            'manufacturers',
            mfr_id
        )

    # SALES CHANNEL IMAGES:

    def get_sales_channel_images(
            self,
            sc_id
    ):
        response = self._get(
            'sales_channels',
            sc_id,
            'images'
        )
        return response.get('sales_channel_images', [])

    def get_sales_channel_image(
            self,
            sc_id,
            img_id
    ):
        return self._get(
            'sales_channels',
            sc_id,
            'images',
            img_id,
        )

    def add_sales_channel_image(
            self,
            sc_id,
            data
    ):
        return self._post(
            'sales_channels',
            sc_id,
            'images',
            **data
        )

    def update_sales_channel_image(
            self,
            sc_id,
            img_id,
            data
    ):
        return self._put(
            'sales_channels',
            sc_id,
            'images',
            img_id,
            **data
        )

    def delete_sales_channel_image(
            self,
            sc_id,
            img_id
    ):
        return self._delete(
            'sales_channels',
            sc_id,
            'images',
            img_id,
        )

    # COLLECTIONS:

    def get_collections(
            self
    ):
        response = self._get(
            'collections'
        )
        return response.get('collections', [])

    def add_collection(
            self,
            data
    ):
        return self._post(
            'collections',
            **data
        )

    def get_collection(
            self,
            collection_id
    ):
        return self._get(
            'collections',
            collection_id
        )

    def update_collection(
            self,
            collection_id,
            data
    ):
        return self._put(
            'collections',
            collection_id,
            **data
        )

    def delete_collection(
            self,
            collection_id
    ):
        return self._delete(
            'collections',
            collection_id
        )

    def add_products_to_collection(
            self,
            collection_id,
            data
    ):
        return self._post(
            'collections',
            collection_id,
            **data
        )

    def remove_products_from_collection(
            self,
            collection_id,
            data
    ):
        return self._delete(
            'collections',
            collection_id,
            'products',
            **data
        )

    # GROUPS:

    def add_group(self, data):
        return self._post(
            'groups',
            **data
        )

    def get_group(
            self,
            group_id
    ):
        return self._get(
            'groups',
            group_id
        )

    def get_groups(
            self,
            mfr_id,
            data
    ):
        return self._get(
            'manufacturers',
            mfr_id,
            'groups',
            **data
        )

    def update_group(
            self,
            group_id,
            data
    ):
        return self._put(
            'groups',
            group_id,
            **data
        )

    def delete_group(
            self,
            group_id
    ):
        return self._delete(
            'groups',
            group_id
        )

    def add_product_to_group(
            self,
            group_id,
            products_ids
    ):
        return self._post_list(
            products_ids,
            'groups',
            group_id,
            'products'
        )

    def delete_product_from_group(
            self,
            group_id,
            prod_id
    ):
        return self._delete(
            'groups',
            group_id,
            'products',
            prod_id
        )

    # LOGS:

    def get_logs(
            self,
            public_key
    ):
        response = self._get(
            'logs',
            public_key
        )
        return response.get('logs', [])

    # Components:

    def get_components(
            self
    ):
        response = self._get(
            'components'
        )
        return response.get('components', [])

    # Assemblages:

    def get_assemblages(
            self
    ):
        response = self._get(
            'assemblages'
        )
        return response.get('assemblages', [])

    # Categories:

    def get_categories(
            self
    ):
        response = self._get(
            'categories'
        )
        return response.get('categories', [])

    def get_primary_sub_categories(
            self,
            category_name
    ):
        response = self._get(
            'categories',
            category_name
        )
        return response.get('categories', [])

    def get_secondary_sub_categories(
            self,
            category_name,
            primary_sub_category_name,
    ):
        response = self._get(
            'categories',
            category_name,
            primary_sub_category_name
        )
        return response.get('categories', [])
