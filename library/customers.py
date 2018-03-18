import logging


def validate_row(row: dict):
    """
    Validate each row for essential keys and types
    Raises an error if validation fails

    :param row:
    :return:
    """

    essential_keys = ['user_id', 'latitude', 'longitude', 'name']
    if len(set(row.keys()).intersection(essential_keys)) < len(essential_keys):
        raise AttributeError("Missing essential keys")

    int(row['user_id'])
    float(row['latitude'])
    float(row['longitude'])
    str(row['name'])


def process_rows(rows: str) -> list:
    """
    Given a list of customers and return a list of dicts, sorted by distance from HQ
    Distance is saved as 'distance_hq'

    :param rows:
    :return:
    """
    import json
    from library.distance import distance_from_hq

    customers = []

    for str in rows:
        try:
            row = json.loads(str)
            validate_row(row)  # Validate the data before adding it in

            row['distance_hq'] = distance_from_hq(float(row['latitude']), float(row['longitude']))
            customers.append(row)

            logging.debug(row)
        except (ValueError, AttributeError) as e:
            # Can't load a row? Print it to err and move forward
            logging.error("'{}' {}".format(str.rstrip(), e))

    """
    Return the list sorted by distance. This has 2 advantages 

    1. Lookups can use a binary search (O(logn)) implementation.
    2. Array slices can be returned, instead of allocating a new array for search results.
    """

    return sorted(customers, key=lambda row: row['distance_hq'])


def load_customers(filename: str) -> list:
    """
    Load customers off `filename` and return a list of dicts, sorted by distance from HQ
    Distance is saved as 'distance_hq'

    :param filename:
    :return: list of dicts of customers
    """

    rows = []
    with open(filename, "r") as fp:
        for str in fp:
            rows.append(str)

    return process_rows(rows)


def find(customers: list, distance: int) -> list:
    """
    Find customers within a `distance` km radius

    :param customers: list of dicts, one dict per customer
    :param distance: Distance in kms
    :return: list of customers within `distance`
    """

    return sorted([c for c in customers if c['distance_hq'] < distance], key=lambda row: row['user_id'])
