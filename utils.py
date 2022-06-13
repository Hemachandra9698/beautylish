from typing import Dict, Any
from collections import OrderedDict


# Ref: https://www.moesif.com/blog/technical/api-design/REST-API-Design-Filtering-Sorting-and-Pagination/#multi-column-sort
# Example: GET /users?sort_by=+email and GET /users?sort_by=-email
# Don't forget to encode plus sign in html request
def parse_sort_by_arg(sort_by_arg: str) -> Dict[str, Any]:
    sort_by = OrderedDict()
    if sort_by_arg is None:
        return sort_by

    sort_str_list = [arg.strip() for arg in sort_by_arg.split(",") if arg.strip() != ""]
    # if arg starts with '+' then we have to sort on asc and if it starts with '-' then we have to sort it on desc.
    # if no '+' or '-' then the request is invalid
    for sort_str in sort_str_list:
        if sort_str.startswith("+"):
            sort_by[sort_str[1:]] = True
        elif sort_str.startswith("-"):
            sort_by[sort_str[1:]] = False
        else:
            raise ValueError("Malformed sort by argument!")

    return sort_by
