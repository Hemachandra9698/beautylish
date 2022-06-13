# Beautylish

## Run the Server
```sh
python -m venv .venv
.\.venv\scripts\activate
pip install -r requirements.txt
python app.py
```

## API Design
REST API
* GET `/products` - to get all products in a table. Can take filter and sort arguments
* GET `/statistics` - to get all statistics. Can take filter arguments
* GET `/` - renders home page which is combination of API `/products` and `/statistics`

## Understanding Sort and Filter
Sorting
* We have given feature for sorting on asc and desc. For identifying which param to be sorted in asc and which one in desc,
we request user to provide '+' for asc infront of the sort param and '-' for desc infront of sort param.
```
# For example for sorting the products by price in asc and by brand_name in desc, we can run the following url
http://127.0.0.1:5001/products?sort_by=%2bprice,-product_name

Please note that the %2b is encoded as '+' by request object.
```
Filtering
* Currently, we are  allowing to filter the products only on 'status' parameter.
* we are taking the values for 'status' param as 'hidden', 'deleted' and 'active'.
* If the user needs only active elements (means which are not hidden or deleted) then he must provide
status=active in the URL
```
# For example we can use the below URL for getting only active products
http://127.0.0.1:5001/products?status=active

# Sort by brand_name in asc and get only active products
http://127.0.0.1:5001/?sort_by=%2bbrand_name&status=active

```

### Examples
```
# Get all products, by default you get all products and un-sorted
http://127.0.0.1:5001/products

# Get all products that are active
http://127.0.0.1:5001/products?status=active

# Get all products that are hidden
http://127.0.0.1:5001/products?status=hidden

# Get all products sorted by price asc
http://127.0.0.1:5001/products?sort_by=%2bprice

# Get all products sorted by price asc and product name desc
http://127.0.0.1:5001/products?sort_by=%2bprice,-product_name

# Get all products that are active and sorted by product name asc
http://127.0.0.1:5001/products?sort_by=%2bproduct_name&status=active

# Home page API
http://127.0.0.1:5001/?sort_by=%2bbrand_name&status=active
```

## Solution
This is the URL for the required requirements
```
http://127.0.0.1:5001/?sort_by=%2bprice,%2bproduct_name&status=active
```

### Note
```
If you run the following URL, you get an unsorted, unfiltered data.
And so the (Statistics for Final sorted removed duplicates/hidden list) and (Statistics for Original Product list)
will be same as there is no filter args or sort args provided. 
That is raw product data

http://127.0.0.1:5001/
```