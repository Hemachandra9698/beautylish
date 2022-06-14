from flask import Flask, request, render_template

from datasource.rest import RestDataSource
from models.product import ProductStatus
from utils import parse_sort_by_arg

app = Flask(__name__)


def get_stats_for_filtered_and_org_products(org_products=None, filtered_products=None):
    """
    gets statistics for both filtered and original products. If they are not provided get a whole
    new product data. You can also filter based on filter_args.
    :param org_products: original unfiltered and unsorted products list
    :param filtered_products: filtered products list on filter_args
    :return: dict of stats and stats template
    """
    # Get filter arguments. Allow to filter only on "product status"
    filter_args = {}
    status_str = request.args.get("status")
    if status_str is not None:
        status = ProductStatus[status_str.upper()]
        filter_args["status"] = status

    stats = datasource.get_statistics(filter_args, org_products, filtered_products)
    return {'stats': stats, 'stats_template': "statistics.html"}


def get_org_products_and_filtered_sorted_products():
    """
    gets the raw product data, filters based on status and sorts the products based on sort_args provided
    :return: dict of original_products which are unfiltered and unsorted, filtered_sorted_products lst,
    products template name, column names var
    """
    # Get filter arguments. Allow to filter only on "product status"
    filter_args = {}
    status_str = request.args.get("status")
    if status_str is not None:
        status = ProductStatus[status_str.upper()]
        filter_args["status"] = status

    # Get sort param
    sort_by_str = request.args.get("sort_by")
    # form the sort dict
    sort_args = parse_sort_by_arg(sort_by_str)
    # get products filtered and sorted
    filtered_sorted_products, org_products = datasource.get_products(filter_args, sort_args)
    # convert Enum values to represent only name
    for product in filtered_sorted_products:
        product['status'] = product['status'].name

    col_names = [
        "product_id",
        "price",
        "product_name",
        "brand_name",
        "status",
    ]
    return {'org_products': org_products, 'filtered_sorted_products': filtered_sorted_products,
            'products_template': 'products_table.html', 'col_names': col_names}


@app.route("/statistics", methods=["GET"])
def get_statistics():
    """
    gets invoked when opened https://<host>:<port>/statistics
    gets statistics for both filtered and unfiltered products.
    statistics -> no of unique products, no of unique brands, avg of price
    :return: html template that shows the statistics of the filtered and unfiltered products
    """
    result_context = get_stats_for_filtered_and_org_products()
    return render_template(
        result_context.get('stats_template', 'statistics.html'),
        stats=result_context['stats']
    )


@app.route("/products", methods=["GET"])
def get_products():
    """
    gets invoked when opened https://<host>:<port>/products
    gets raw_product_data or filtered and sorted based on whether 'status' and 'sort_by' params are provided. If not provided then not filtered
    or not sorted
    :return: html template that shows the table of products
    """
    result_context = get_org_products_and_filtered_sorted_products()
    return render_template(
        result_context.get('products_template', 'products_table.html'),
        records=result_context['filtered_sorted_products'],
        col_names=result_context['col_names']
    )


@app.route("/")
def index():
    """
    gets invoked when opened https://<host>:<port>/
    :return: html template that shows unsorted-unfiltered products and statistics of the products
    If the params -> filter_by and sort_by are provided then the products get filtered and sorted in the provided manner.
    """
    # get products filtered and sorted
    products_context = get_org_products_and_filtered_sorted_products()
    # get statistics for original unfiltered and filtered products
    stats_context = get_stats_for_filtered_and_org_products(
        org_products=products_context['org_products'],
        filtered_products=products_context['filtered_sorted_products']
    )
    return render_template(
        products_context.get('products_template', 'products_table.html'),
        records=products_context['filtered_sorted_products'],
        col_names=products_context['col_names']
    ) + render_template(
        stats_context.get('stats_template', 'statistics.html'),
        stats=stats_context['stats']
    )


# Globals
PORT = 5001
BEAUTYLISH_REST_API_URL = "https://www.beautylish.com/rest/interview-product/list/"
datasource = RestDataSource(BEAUTYLISH_REST_API_URL)


def main():
    """
    runs the flask server on the provided host and port
    :return:
    """
    app.run(host="0.0.0.0", port=PORT, debug=True)


if __name__ == "__main__":
    main()
