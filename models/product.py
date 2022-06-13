import enum


class ProductStatus(enum.Enum):
    ACTIVE = 0
    HIDDEN = 1
    DELETED = 2


class Product:
    def __init__(
        self,
        product_id: int,
        price: float,
        brand_name: str,
        product_name: str,
        status: ProductStatus,
    ):
        self.product_id = product_id
        self.price = price
        self.brand_name = brand_name
        self.product_name = product_name
        self.status = status

    def __hash__(self):
        return hash(
            (
                self.product_id,
                self.price,
                self.brand_name,
                self.product_name,
                self.status,
            )
        )

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplementedError()
        return (
            self.product_id == other.product_id
            and self.price == other.price
            and self.brand_name == other.brand_name
            and self.product_name == other.product_name
            and self.status == other.status
        )

    def __str__(self):
        return "Id: {},  BrandName: {},  ProductName: {},  Price: {}, Status: {}".format(
            self.product_id, self.brand_name, self.product_name, self.price, self.status
        )

    def __setitem__(self, key, value):
        vars(self)[key] = value

    def __getitem__(self, item):
        """
        to make the Product object subscriptable
        :param item: name of the instance var
        :return: attribute value of the instance var item
        """
        return super().__getattribute__(item)
