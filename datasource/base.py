from typing import Optional, List, Dict, Any, OrderedDict

from models.product import Product


class DataSource:
    data_source_name = None  # type: Optional[str]

    def get_raw_product_data(self) -> List[Product]:
        raise NotImplementedError("Method get_raw_product_data() is not implemented.")

    def get_processed_product_data(self) -> List[Product]:
        raise NotImplementedError(
            "Method get_processed_product_data() is not implemented."
        )

    def get_products(
        self,
        filter_by: Dict[str, Any],
        sort_by: OrderedDict[str, bool],
    ) -> List[Product]:
        raise NotImplementedError("Method get_products() is not implemented.")

    def get_statistics(self, filter_by: Dict[str, Any],
                       org_products: List[Product],
                       filtered_products: List[Product]) -> Dict[str, Any]:
        raise NotImplementedError("Method get_statistics() is not implemented.")
