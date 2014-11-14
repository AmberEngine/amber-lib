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
    headers=None,
    user_identifier=None,
    user_manufacturer_id=None
):
    retries = 3
    r = False
    while retries > 0:
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
            'api_key': public_key,
            'user_identifier': user_identifier,
            'user_manufacturer_id': user_manufacturer_id
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
            return json.loads(r.text)
        else:
            retries -= 1
    try:
        raise AmberError(r.status_code, json.loads(r.text))
    except ValueError:
        raise AmberError(r.status_code, r.text)


class AmberClient(object):

    def init(self, api_url, pub_key, pri_key):
        self.api_url = api_url
        self.pub_key = pub_key
        self.pri_key = pri_key

    def _url(self, *path):
        return self.api_url + "/api/v1/" + "/".join([str(x) for x in path])

    def _get(self, user_identifier, user_manufacturer_id, *path, **data):
        url = self._url(*path)
        headers = {'Content-Type': 'application/json'}
        args = {
            'url': url,
            'public_key': self.pub_key,
            'private_key': self.pri_key,
            'method': 'GET',
            'data': json.dumps(data, cls=ObjectEncoder),
            'headers': headers,
            'user_identifier': user_identifier,
            'user_manufacturer_id': user_manufacturer_id,
        }
        return _send_request(**args)

    def _post(self, user_identifier, user_manufacturer_id, *path, **data):
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
            'headers': headers,
            'user_identifier': user_identifier,
            'user_manufacturer_id': user_manufacturer_id,
        }
        return _send_request(**args)

    def _post_list(
            self,
            user_identifier,
            user_manufacturer_id,
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
            'headers': headers,
            'user_identifier': user_identifier,
            'user_manufacturer_id': user_manufacturer_id,
        }
        return _send_request(**args)

    def _put(self, user_identifier, user_manufacturer_id, *path, **data):
        url = self._url(*path)
        headers = {'Content-Type': 'application/json'}
        args = {
            'url': url,
            'public_key': self.pub_key,
            'private_key': self.pri_key,
            'method': 'PUT',
            'data': json.dumps(data, cls=ObjectEncoder),
            'headers': headers,
            'user_identifier': user_identifier,
            'user_manufacturer_id': user_manufacturer_id,
        }
        return _send_request(**args)

    def _delete(self, user_identifier, user_manufacturer_id, *path, **data):
        url = self._url(*path)
        headers = {'Content-Type': 'application/json'}
        args = {
            'url': url,
            'public_key': self.pub_key,
            'private_key': self.pri_key,
            'method': 'DELETE',
            'data': json.dumps(data, cls=ObjectEncoder),
            'headers': headers,
            'user_identifier': user_identifier,
            'user_manufacturer_id': user_manufacturer_id,
        }
        return _send_request(**args)

    def _search(self, user_identifier, user_manufacturer_id, *path, **data):
        url = self._url(*path)
        headers = {'Content-Type': 'application/json'}
        args = {
            'url': url,
            'public_key': self.pub_key,
            'private_key': self.pri_key,
            'method': 'POST',
            'data': json.dumps(data, cls=ObjectEncoder),
            'headers': headers,
            'user_identifier': user_identifier,
            'user_manufacturer_id': user_manufacturer_id,
        }
        return _send_request(**args)

    def update_ngram_index(
            self,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            'update_ngram_index',
            user_identifier,
            user_manufacturer_id
        )

    # PRODUCT:

    def get_product(
            self,
            prod_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'products',
            prod_id
        )

    def get_product_component(
            self,
            prod_id,
            component_name,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'products',
            prod_id,
            'component',
            component_name
        )

    def get_products(
            self,
            params,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'products',
            **params
        )

    def search_products(
            self,
            params,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._search(
            user_identifier,
            user_manufacturer_id,
            'products',
            'search',
            **params
        )

    def add_product(
            self,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._post(
            user_identifier,
            user_manufacturer_id,
            'products',
            **data
        )

    def update_product(
            self,
            prod_id,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._put(
            user_identifier,
            user_manufacturer_id,
            'products',
            prod_id,
            **data
        )

    def update_product_component(
            self,
            prod_id,
            component_name,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._put(
            user_identifier,
            user_manufacturer_id,
            'products',
            prod_id,
            'component',
            component_name,
            **data
        )

    def get_product_sub_component(
            self,
            prod_id,
            component_name,
            sub_component_data_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'products',
            prod_id,
            'sub_component',
            component_name,
            sub_component_data_id,
        )

    def add_product_sub_component(
            self,
            prod_id,
            component_name,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._post(
            user_identifier,
            user_manufacturer_id,
            'products',
            prod_id,
            'sub_component',
            component_name,
            **data
        )

    def update_product_sub_component(
            self,
            prod_id,
            component_name,
            sub_component_data_id,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._put(
            user_identifier,
            user_manufacturer_id,
            'products',
            prod_id,
            'sub_component',
            component_name,
            sub_component_data_id,
            **data
        )

    def delete_product_sub_component(
            self,
            prod_id,
            component_name,
            sub_component_data_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._delete(
            user_identifier,
            user_manufacturer_id,
            'products',
            prod_id,
            'sub_component',
            component_name,
            sub_component_data_id
        )

    def delete_product(
            self,
            prod_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._delete(
            user_identifier,
            user_manufacturer_id,
            'products',
            prod_id
        )

    def delete_products(
            self,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._delete(
            user_identifier,
            user_manufacturer_id,
            'products',
            **data
        )

    def add_products_to_collection(
            self,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._put(
            user_identifier,
            user_manufacturer_id,
            'products',
            'add_collection',
            **data
        )

    def remove_products_from_collection(
            self,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._put(
            user_identifier,
            user_manufacturer_id,
            'products',
            'remove_collection',
            **data
        )

    # IMAGES:

    def get_images(
            self,
            prod_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'products',
            prod_id,
            'images'
        )

    def add_image(
            self,
            prod_id,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._post(
            user_identifier,
            user_manufacturer_id,
            'products',
            prod_id,
            'images',
            **data
        )

    def get_image(
            self,
            img_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'image',
            img_id
        )

    def edit_image(
            self,
            img_id,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._put(
            user_identifier,
            user_manufacturer_id,
            'image',
            img_id,
            **data
        )

    def delete_image(
            self,
            img_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._delete(
            user_identifier,
            user_manufacturer_id,
            'image',
            img_id
        )

    # MANUFACTURER IMAGES:

    def get_manufacturer_images(
            self,
            mfr_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'manufacturers',
            mfr_id,
            'manufacturer_images'
        )

    def add_manufacturer_image(
            self,
            mfr_id,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._post(
            user_identifier,
            user_manufacturer_id,
            'manufacturers',
            mfr_id,
            'manufacturer_images',
            **data
        )

    def get_manufacturer_image(
            self,
            mfr_id,
            mfr_img_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'manufacturers',
            mfr_id,
            'manufacturer_images',
            mfr_img_id
        )

    def edit_manufacturer_image(
            self,
            mfr_id,
            mfr_img_id,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._put(
            user_identifier,
            user_manufacturer_id,
            'manufacturers',
            mfr_id,
            'manufacturer_images',
            mfr_img_id,
            **data
        )

    def delete_manufacturer_image(
            self,
            mfr_id,
            mfr_img_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._delete(
            user_identifier,
            user_manufacturer_id,
            'manufacturers',
            mfr_id,
            'manufacturer_images',
            mfr_img_id
        )

    # OPTION SETS:

    def get_option_sets(
            self,
            manufacturer_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'option_sets',
            manufacturer_id
        )

    def add_option_set(
            self,
            manufacturer_id,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._post(
            user_identifier,
            user_manufacturer_id,
            'option_sets',
            manufacturer_id,
            **data
        )

    def get_option_set(
            self,
            option_set_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'option_set',
            option_set_id
        )

    def edit_option_set(
            self,
            option_set_id,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._put(
            user_identifier,
            user_manufacturer_id,
            'option_set',
            option_set_id,
            **data
        )

    def delete_option_set(
            self,
            option_set_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._delete(
            user_identifier,
            user_manufacturer_id,
            'option_set',
            option_set_id
        )

    # OPTIONS:

    def get_options(
            self,
            option_set_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'option_set',
            option_set_id,
            'options'
        )

    def add_option(
            self,
            option_set_id,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._post(
            user_identifier,
            user_manufacturer_id,
            'option_set',
            option_set_id,
            'options',
            **data
        )

    def get_option(
            self,
            option_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'option',
            option_id
        )

    def edit_option(
            self,
            option_id,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._put(
            user_identifier,
            user_manufacturer_id,
            'option',
            option_id,
            **data
        )

    def delete_option(
            self,
            option_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._delete(
            user_identifier,
            user_manufacturer_id,
            'option',
            option_id
        )

    # TAGS:

    def get_tags(
            self,
            prod_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'products',
            prod_id,
            'tags'
        )

    def delete_tag(
            self,
            prod_id,
            tag_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._delete(
            user_identifier,
            user_manufacturer_id,
            'products',
            prod_id,
            'tags',
            tag_id
        )

    def add_tags(
            self,
            prod_id,
            new_tags,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._post_list(
            user_identifier,
            user_manufacturer_id,
            new_tags,
            'products',
            prod_id,
            'tags'
        )

    # MANUFACTURER:

    def get_manufacturer(
            self,
            mfr_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'manufacturers',
            mfr_id
        )

    def get_manufacturers(
            self,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'manufacturers',
            **data
        )

    def add_manufacturer(
            self,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._post(
            user_identifier,
            user_manufacturer_id,
            'manufacturers',
            **data
        )

    def update_manufacturer(
            self,
            mfr_id,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._put(
            user_identifier,
            user_manufacturer_id,
            'manufacturers',
            mfr_id,
            **data
        )

    # API KEY:

    def get_roles(self, user_identifier=None, user_manufacturer_id=None):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'role'
        )

    def get_api_key(
            self,
            api_key_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'api_keys',
            api_key_id
        )

    def get_api_keys(self, user_identifier=None, user_manufacturer_id=None):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'api_keys'
        )

    def add_api_key(
            self,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._post(
            user_identifier,
            user_manufacturer_id,
            'api_keys',
            **data
        )

    def update_api_key(
            self,
            api_key_id,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._put(
            user_identifier,
            user_manufacturer_id,
            'api_keys',
            api_key_id,
            **data
        )

    def delete_api_key(
            self,
            api_key_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._delete(
            user_identifier,
            user_manufacturer_id,
            'api_keys',
            api_key_id
        )

    # USER (deprecated):

    def get_user(
            self,
            api_key_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'api_keys',
            api_key_id
        )

    # SALES CHANNELS:

    def get_sales_channels(
            self,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'sales_channels'
        )

    def get_sales_channel(
            self,
            sc_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'sales_channels',
            sc_id
        )

    def add_sales_channel(
            self,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._post(
            user_identifier,
            user_manufacturer_id,
            'sales_channels',
            **data
        )

    def update_sales_channel(
            self,
            sc_id,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._put(
            user_identifier,
            user_manufacturer_id,
            'sales_channels',
            sc_id,
            **data
        )

    def delete_sales_channel(
            self,
            sc_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._delete(
            user_identifier,
            user_manufacturer_id,
            'sales_channels',
            sc_id
        )

    def sales_channel_get_product(
            self,
            sc_id,
            mfr_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'sales_channels',
            sc_id,
            'manufacturers',
            mfr_id
        )

    def sales_channel_add_product(
            self,
            sc_id,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._put(
            user_identifier,
            user_manufacturer_id,
            'sales_channels',
            sc_id,
            'add_product',
            **data
        )

    def sales_channel_remove_product(
            self,
            sc_id,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._put(
            user_identifier,
            user_manufacturer_id,
            'sales_channels',
            sc_id,
            'remove_product',
            **data
        )

    def sales_channel_add_manufacturer(
            self,
            sc_id,
            mfr_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._put(
            user_identifier,
            user_manufacturer_id,
            'sales_channels',
            sc_id,
            'add_manufacturer',
            mfr_id
        )

    def sales_channel_remove_manufacturer(
            self,
            sc_id,
            mfr_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._put(
            user_identifier,
            user_manufacturer_id,
            'sales_channels',
            sc_id,
            'remove_manufacturer',
            mfr_id
        )

    # SALES CHANNEL IMAGES:

    def get_sales_channel_images(
            self,
            sc_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'sales_channels',
            sc_id,
            'images'
        )

    def get_sales_channel_image(
            self,
            sc_id,
            img_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'sales_channels',
            sc_id,
            'images',
            img_id,
        )

    def add_sales_channel_image(
            self,
            sc_id,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._post(
            user_identifier,
            user_manufacturer_id,
            'sales_channels',
            sc_id,
            'images',
            **data
        )

    def update_sales_channel_image(
            self,
            sc_id,
            img_id,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._put(
            user_identifier,
            user_manufacturer_id,
            'sales_channels',
            sc_id,
            'images',
            img_id,
            **data
        )

    def delete_sales_channel_image(
            self,
            sc_id,
            img_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._delete(
            user_identifier,
            user_manufacturer_id,
            'sales_channels',
            sc_id,
            'images',
            img_id,
        )

    # COLLECTIONS:

    def get_collections(
            self,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'collections'
        )

    def add_collection(
            self,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._post(
            user_identifier,
            user_manufacturer_id,
            'collections',
            **data
        )

    def get_collection(
            self,
            collection_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'collections',
            collection_id
        )

    def update_collection(
            self,
            collection_id,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._put(
            user_identifier,
            user_manufacturer_id,
            'collections',
            collection_id,
            **data
        )

    def delete_collection(
            self,
            collection_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._delete(
            user_identifier,
            user_manufacturer_id,
            'collections',
            collection_id
        )

    # GROUPS:

    def add_group(self, data, user_identifier=None, user_manufacturer_id=None):
        return self._post(
            user_identifier,
            user_manufacturer_id,
            'groups',
            **data
        )

    def get_group(
            self,
            group_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'groups',
            group_id
        )

    def get_groups(
            self,
            mfr_id,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'manufacturers',
            mfr_id,
            'groups',
            **data
        )

    def update_group(
            self,
            group_id,
            data,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._put(
            user_identifier,
            user_manufacturer_id,
            'groups',
            group_id,
            **data
        )

    def delete_group(
            self,
            group_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._delete(
            user_identifier,
            user_manufacturer_id,
            'groups',
            group_id
        )

    def add_product_to_group(
            self,
            group_id,
            products_ids,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._post_list(
            user_identifier,
            user_manufacturer_id,
            products_ids,
            'groups',
            group_id,
            'products'
        )

    def delete_product_from_group(
            self,
            group_id,
            prod_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._delete(
            user_identifier,
            user_manufacturer_id,
            'groups',
            group_id,
            'products',
            prod_id
        )

    # LOGS:

    def get_logs(
            self,
            user_id,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'logs',
            user_id=user_id
        )

    # Components:

    def get_components(
            self,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'components'
        )

    # Assemblages:

    def get_assemblages(
            self,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'assemblages'
        )

    # Categories:

    def get_categories(
            self,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'categories'
        )

    def get_primary_sub_categories(
            self,
            category_name,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'categories',
            category_name
        )

    def get_secondary_sub_categories(
            self,
            category_name,
            primary_sub_category_name,
            user_identifier=None,
            user_manufacturer_id=None
    ):
        return self._get(
            user_identifier,
            user_manufacturer_id,
            'categories',
            category_name,
            primary_sub_category_name
        )
