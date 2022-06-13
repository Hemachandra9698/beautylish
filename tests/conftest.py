# contains fixtures used by pytest and automatically used in test classes

import copy
import pytest

from datasource.rest import RestDataSource
from models.product import Product, ProductStatus


@pytest.fixture(scope='function')
def raw_product_data():
    product_data = [
        {"deleted": False, "price": "$123.45", "brand_name": "Wonderful Widgets", "id": 1001, "hidden": False,
         "product_name": "Most Wonderful Widget"},
        {"deleted": True, "price": "$10.00", "brand_name": "Acme", "id": 2003, "hidden": False,
         "product_name": "Anvil - Two Pack"},
        {"deleted": False, "price": "$123.45", "brand_name": "Acme", "id": 2000, "hidden": False,
         "product_name": "Anvil"},
        {"deleted": False, "price": "$123.45", "brand_name": "Wonderful Widgets", "id": 1000, "hidden": False,
         "product_name": "Widget 3000"},
        {"deleted": False, "price": "$123.45", "brand_name": "Wonderful Widgets", "id": 1001, "hidden": False,
         "product_name": "Most Wonderful Widget"},
        {"deleted": False, "price": "$123.45", "brand_name": "Hooli", "id": 2004, "hidden": False,
         "product_name": "Nucleus"},
        {"deleted": False, "price": "$123.45", "brand_name": "Hooli", "id": 2004, "hidden": False,
         "product_name": "Nucleus"},
        {"deleted": False, "price": "$10.00", "brand_name": "Acme", "id": 2001, "hidden": False,
         "product_name": "Giant Anvil"},
        {"deleted": False, "price": "$10.00", "brand_name": "Acme", "id": 2002, "hidden": False,
         "product_name": "Mini Anvil"}
    ]
    return product_data


@pytest.fixture(scope='function')
def get_product_lst(raw_product_data):
    """
    construct list of products from raw_product_data
    :param raw_product_data: mock raw product data
    :return: list of products
    """
    status_dict = {'deleted': ProductStatus.DELETED, 'hidden': ProductStatus.HIDDEN}
    product_lst = []

    for data in copy.deepcopy(raw_product_data):
        if data['deleted']:
            status = status_dict['deleted']
        elif data['hidden']:
            status = status_dict['hidden']
        else:
            status = ProductStatus.ACTIVE

        data['price'] = float(data['price'].replace("$", "").replace(",", ""))

        product_lst.append(
            Product(data['id'], data['price'], data['brand_name'], data['product_name'], status)
        )
    return product_lst


@pytest.fixture(scope='function')
def rest_data_source_obj():
    """
    creates object for RestDataSource class
    :return: RestDataSource class object
    """
    base_url = "https://www.beautylish.com/rest/interview-product/list/"
    data_source = RestDataSource(base_url)
    return data_source


@pytest.fixture(scope='function')
def get_active_prods(get_product_lst):
    """
    get products which are marked as active
    :param get_product_lst: fixture which returns list of products
    :return: list of products that are active
    """
    return [
        product for product in get_product_lst if product['status'] == ProductStatus.ACTIVE
    ]


@pytest.fixture(scope='function')
def get_deleted_prods(get_product_lst):
    """
    get products which are marked as deleted
    :param get_product_lst: fixture which returns list of products
    :return: list of products that are deleted
    """
    return [
        product for product in get_product_lst if product['status'] == ProductStatus.DELETED
    ]


@pytest.fixture(scope='function')
def get_hidden_prods(get_product_lst):
    """
    get products which are marked as hidden
    :param get_product_lst: fixture which returns list of products
    :return: list of products that are hidden
    """
    return [
        product for product in get_product_lst if product['status'] == ProductStatus.HIDDEN
    ]