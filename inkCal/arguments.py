import argparse

def get():

    parser = argparse.ArgumentParser()
    parser.add_argument("--log", default="warning", help="Log level, INFO, WARN, ERROR, DEBUG.")
    return parser.parse_args()


    zz = args

    print("ZZ", zz)

    logging.info("INFO0")
    logging.error("E0")

    log = logging.getLogger("app1")
    log.setLevel(level=args.log.upper())
    log.info("Test1")

    log.debug("Debug1")

    log.error("E1")

    print("HEJ!")
