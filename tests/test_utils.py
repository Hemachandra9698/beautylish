import pytest
from collections import OrderedDict

from utils import parse_sort_by_arg


class TestUtils:
    @pytest.mark.parametrize("sort_by_arg, expected_response", [
        ("+price,-brand_name", OrderedDict({'price': True, 'brand_name': False})),
        ("+price,+brand_name", OrderedDict({'price': True, 'brand_name': True})),
        ("-price,+product_name", OrderedDict({'price': False, 'product_name': True})),
        ("-price,-product_name", OrderedDict({'price': False, 'product_name': False})),
        (None, OrderedDict())
    ])
    def test_parse_sort_by_arg(self, sort_by_arg, expected_response):
        received_response = parse_sort_by_arg(sort_by_arg)
        assert expected_response == received_response

    def test_parse_sort_by_arg_when_error_returned(self):
        # check if parse_sort_by_arg() raises ValueError when incorrect sort_by_arg is provided
        sort_by_arg = "%2bprice,-brand_name"
        with pytest.raises(ValueError) as exception_context:
            parse_sort_by_arg(sort_by_arg)
            