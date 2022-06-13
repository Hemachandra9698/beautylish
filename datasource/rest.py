import requests
from typing import List, Any, Dict, OrderedDict, Tuple

from datasource.base import DataSource
from models.product import Product, ProductStatus


class InvalidResponseError(Exception):
    def __init__(self, msg):
        self.msg = msg


class RestDataSource(DataSource):
    data_source_name = "REST"

    def __init__(self, base_url):
        super().__init__()
        self.response = None
        self.base_url = base_url

    def _convert_dollar_to_float_format(self, price):
        return float(price.replace("$", "").replace(",", ""))

    def get_data_from_api(self) -> List[Dict[str, Any]]:
        """
        connects to the base_url and gets the product list. Change this for connecting to Database
        :return: products_list json or raises InvalidResponseError if got a wrong response from BASE_URL
        """
        self.response = requests.get(url=self.base_url)
        if self.response.status_code == 200:
            data = self.response.json()["products"]
            return data
        raise InvalidResponseError("Unable to get products from the URL")

    def get_raw_product_data(self) -> List[Product]:
        """
        gets the raw data by connecting to the URL and assign the status as provided. If the product is deleted
        we need not bother about whether it is hidden or not. If deleted, change the status to deleted,
        if hidden then change the status to hidden, else the status will be active.
        :return: list of product objects
        """
        products = []
        for item in self.get_data_from_api():
            item_status = ProductStatus.ACTIVE
            if item["deleted"]:
                item_status = ProductStatus.DELETED
            elif item["hidden"]:
                item_status = ProductStatus.HIDDEN

            products.append(
                Product(
                    item["id"],
                    self._convert_dollar_to_float_format(item["price"]),
                    item["brand_name"],
                    item["product_name"],
                    item_status,
                )
            )
        return products

    def get_processed_product_data(self) -> List[Product]:
        """
        remove duplicates from list of products
        :return: distinct list of products
        """
        products = self.get_raw_product_data()
        # removing duplicates from here itself
        return list(set(products))

    # Filter products
    def filter(self, products, filter_by) -> List[Product]:
        """
        For now we are filtering the elements based on status only
        :param products: list of products
        :param filter_by: dict with key as sort param matching with Product class variable and its value for matching
        :return: list of filtered products, only contains the matched filter criteria. For now only that match with the status value provided.
        """
        final_products = []
        for product in products:
            for k, v in filter_by.items():
                if getattr(product, k, None) != v:
                    break
            else:
                final_products.append(product)
        return final_products

    # Sort products
    # Ref: https://stackoverflow.com/questions/11206884/how-to-write-sort-key-functions-for-descending-values
    def sort(self, products, sort_by) -> List[Product]:
        """
        sort the products based on sort_by arg. Make sure you give str keys at last and integer keys at first
        :param products: list of product objects
        :param sort_by: dict of sort params by which we sort the products
        :return:
        """
        final_products = list(products)
        # iterate over the sort items and sort once per key
        for key, asc in reversed(sort_by.items()):
            final_products = sorted(final_products, key=lambda x: x[key], reverse=not asc)
        return final_products

    def get_products(
        self,
        filter_by: Dict[str, Any],
        sort_by: OrderedDict[str, bool],
    ) -> tuple[list[Product], list[Product]]:
        """
        get the raw product data, remove duplicates and filter them on status col. Finally, Sort the list.
        :param filter_by: dict of filter items by which we filter the list of products
        :param sort_by: dict of sort params by which we sort the products
        :return: final list of products that are filtered and sorted
        """
        # get unique/distinct products after removing any duplicates
        org_products = self.get_processed_product_data()
        # filter based on status and sort the output list on sort_by items
        return self.sort(
            self.filter(org_products, filter_by),
            sort_by
        ), org_products

    def get_statistics(self, filter_by: Dict[str, Any], org_products=None, filtered_products=None) -> Dict[Any, Any]:
        """
        get statistics for both raw product data and sorted_filtered product data
        :param filtered_products: (optional) can send filtered products for getting stats
        :param org_products: (optional) can send original unfiltered products
        :param filter_by: filter by dict by which we filter the raw data. currently we filter only on status
        :return: dict containing statistics for both filtered and un-filtered data
        """
        result = {}

        # Un-filtered
        unfiltered_products = org_products if org_products else self.get_raw_product_data()

        result["unfiltered"] = {
            "nproducts": len(set([product["product_id"] for product in unfiltered_products])),
            "nbrands": len(set([product["brand_name"] for product in unfiltered_products])),
            "avg_price": sum([product["price"] for product in unfiltered_products]) / len(unfiltered_products),
        }

        # Filtered
        filtered_products = filtered_products if filtered_products else self.filter(
            self.get_processed_product_data(),
            filter_by,
        )
        result["filtered"] = {
            "nproducts": len(set([product["product_id"] for product in filtered_products])),
            "nbrands": len(set([product["brand_name"] for product in filtered_products])),
            "avg_price": sum([product["price"] for product in filtered_products]) / len(filtered_products),
        }

        return result
