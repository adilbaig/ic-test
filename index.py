def main(filename, distance):
    from library.customers import load_customers, find

    customers = load_customers(filename)

    for r in sorted(find(customers, distance), key=lambda row: row['user_id']):
        print("{user_id})\t{name} (Dist: {distance_hq:0.3f}km)".format(**r))


def _setup_logger(verbosity: int):
    import logging.config

    # This can come from a config file
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s'))
    logger.addHandler(handler)

    logger = logging.getLogger()
    logger.setLevel(logging.ERROR - (verbosity * 10))


if __name__ == '__main__':
    import argparse, logging

    description = "Invite customers within a given radius to the Intercom HQ. For food, drinks and fun!"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--customers', type=str, default='customers.json',
                        help='A JSON file of customers. Default: "./customers.json"')
    parser.add_argument('--radius', type=int, default=100,
                        help='Invite customers with a `radius`km distance to Intercom! Default: 100')
    parser.add_argument('--debug', dest='debug', action='store_true', help='Print DEBUG output.')

    args = parser.parse_args()
    _setup_logger(logging.DEBUG if args.debug else 0)

    main(args.customers, args.radius)
