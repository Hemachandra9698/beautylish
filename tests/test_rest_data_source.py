import operator

import pytest

from datasource.rest import InvalidResponseError
from models.product import ProductStatus


@pytest.mark.usefixtures("get_product_lst", "rest_data_source_obj")
class TestRestDataSource:
    # we are using requests_mock fixture which is available by default
    def test_get_data_from_api_when_success_is_returned(self, get_product_lst,
                                                        rest_data_source_obj, requests_mock):
        # provide a mock_url
        rest_data_source_obj.base_url = 'mock://test.com'
        # mock the requests.get() method including json
        requests_mock.get('mock://test.com', status_code=200, json={'products': len(get_product_lst)})
        resp = rest_data_source_obj.get_data_from_api()
        assert rest_data_source_obj.response.status_code == 200
        assert resp == len(get_product_lst)

    def test_get_data_from_api_when_error_is_returned(self, rest_data_source_obj, requests_mock):
        # provide a mock_url
        rest_data_source_obj.base_url = 'mock://test.com'
        # mock the requests.get() method including json
        requests_mock.get('mock://test.com', status_code=404)
        # check if error raises
        with pytest.raises(InvalidResponseError):
            rest_data_source_obj.get_data_from_api()

    @pytest.mark.usefixtures("raw_product_data")
    def test_get_raw_product_data(self, rest_data_source_obj, raw_product_data, mocker):
        # patch get_data_from_api() method to return the value of raw_product_data
        mocker.patch(
            'datasource.rest.RestDataSource.get_data_from_api',
            return_value=raw_product_data
        )
        received_response = rest_data_source_obj.get_raw_product_data()
        assert received_response == raw_product_data

    def test_get_processed_product_data(self, rest_data_source_obj, get_product_lst, mocker):
        # patch get_raw_product_data() method to return the value of get_product_lst
        # we already have a duplicate item with id=1001 in get_product_lst fixture.
        # let's send this as a return value
        mocker.patch(
            'datasource.rest.RestDataSource.get_raw_product_data',
            return_value=get_product_lst
        )
        received_response = rest_data_source_obj.get_processed_product_data()
        # we are converting get_product_lst to set for removing duplicates
        assert set(received_response) == set(get_product_lst)

    # we are sending the fixtures as values in expected_response
    @pytest.mark.parametrize("filter_by, expected_response", [
        ({'status': ProductStatus.ACTIVE}, 'get_active_prods'),
        ({'status': ProductStatus.DELETED}, 'get_deleted_prods'),
        ({'status': ProductStatus.HIDDEN}, 'get_hidden_prods'),
    ])
    def test_filter_when_filtered_by_status(self, rest_data_source_obj, get_product_lst,
                                            filter_by, expected_response, request):
        # as we are sending fixtures as strings in expected_response var get those return values
        expected_response = request.getfixturevalue(expected_response)
        # call the func() to be tested
        received_response = rest_data_source_obj.filter(get_product_lst, filter_by)
        assert set(received_response) == set(expected_response)

    def test_sort_on_price_asc(self, rest_data_source_obj, get_product_lst):
        price_sorted_lst = sorted(
            get_product_lst,
            key=operator.itemgetter('price'),
            reverse=False
        )
        # True as value indicates asc and False as desc
        received_response = rest_data_source_obj.sort(get_product_lst, {'price': True})
        for i in range(len(price_sorted_lst)):
            if not (price_sorted_lst[i]['price'] == received_response[i]['price'] and
                    price_sorted_lst[i]['product_id'] == received_response[i]['product_id']):
                raise AssertionError('Sorted lists not matching')

    def test_sort_on_price_and_product_name_asc(self, rest_data_source_obj, get_product_lst):
        price_pname_sorted_lst = sorted(
            get_product_lst,
            key=operator.itemgetter(*['price', 'product_name']),
            reverse=False
        )
        # True as value indicates asc and False as desc
        received_response = rest_data_source_obj.sort(get_product_lst,
                                                      {'price': True, 'product_name': True})
        for i in range(len(price_pname_sorted_lst)):
            if not (price_pname_sorted_lst[i]['price'] == received_response[i]['price'] and
                    price_pname_sorted_lst[i]['product_id'] == received_response[i]['product_id']):
                raise AssertionError('Sorted lists not matching')

    def test_sort_on_price_desc_and_product_name_asc(self, rest_data_source_obj, get_product_lst):
        # sort products on product name asc
        pname_sorted_lst = sorted(
            get_product_lst,
            key=operator.itemgetter('product_name'),
            reverse=False  # sorts on asc
        )
        # sort again on price desc
        price_pname_sorted_lst = sorted(
            pname_sorted_lst,
            key=operator.itemgetter('price'),
            reverse=True  # sorts on desc
        )
        # True as value indicates asc and False as desc
        received_response = rest_data_source_obj.sort(get_product_lst,
                                                      {'price': False, 'product_name': True})
        # compare the response of actual func()
        for i in range(len(price_pname_sorted_lst)):
            if not (price_pname_sorted_lst[i]['price'] == received_response[i]['price'] and
                    price_pname_sorted_lst[i]['product_id'] == received_response[i]['product_id']):
                raise AssertionError('Sorted lists not matching')

    def test_get_products_when_filtered_on_status_and_sorted_by_price_asc(
            self, rest_data_source_obj, get_product_lst, mocker
    ):
        # patch the get_processed_product_data() for getting distinct products
        mocker.patch(
            'datasource.rest.RestDataSource.get_processed_product_data',
            return_value=list(set(get_product_lst))
        )
        # form the expected_response_lst by filtering and sorting it on price
        filtered_products = rest_data_source_obj.filter(list(set(get_product_lst)), {'status': ProductStatus.ACTIVE})
        expected_response_lst = sorted(
            filtered_products,
            key=operator.itemgetter('price'),
            reverse=False
        )
        # call the actual function
        received_response_lst, org_products = rest_data_source_obj.get_products(filter_by={'status': ProductStatus.ACTIVE},
                                                                  sort_by={'price': True})

        # compare the response of actual func()
        for i in range(len(received_response_lst)):
            if not (received_response_lst[i]['price'] == expected_response_lst[i]['price'] and
                    received_response_lst[i]['product_id'] == expected_response_lst[i]['product_id']):
                raise AssertionError('Sorted lists not matching')

    def test_get_statistics_when_filtered_by_status_is_active(self,
                                                              rest_data_source_obj,
                                                              get_product_lst,
                                                              mocker):
        # patch the get_raw_product_data()
        mocker.patch(
            'datasource.rest.RestDataSource.get_raw_product_data',
            return_value=get_product_lst
        )
        unfiltered_products = get_product_lst

        expected_result = {"unfiltered": {
            "nproducts": len(set([product["product_id"] for product in unfiltered_products])),
            "nbrands": len(set([product["brand_name"] for product in unfiltered_products])),
            "avg_price": sum([product["price"] for product in unfiltered_products]) / len(unfiltered_products),
        }}

        # generate expected_filtered_results
        expected_filtered_results = rest_data_source_obj.filter(list(set(get_product_lst)),
                                                        {'status': ProductStatus.ACTIVE})

        expected_result["filtered"] = {
            "nproducts": len(set([product["product_id"] for product in expected_filtered_results])),
            "nbrands": len(set([product["brand_name"] for product in expected_filtered_results])),
            "avg_price": sum([product["price"] for product in expected_filtered_results]) / len(expected_filtered_results),
        }

        # call the main function and get the response
        received_response = rest_data_source_obj.get_statistics({'status': ProductStatus.ACTIVE})

        assert expected_result == received_response
