import logging

def setup_logging(log_filename, log_format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p'):
    # Check if logging is already configured
    if not logging.getLogger().handlers:
        # Set up logging to a file
        logging.basicConfig(filename=log_filename, level=logging.INFO, format=log_format, datefmt=datefmt)

        # Set up logging to the terminal
        stream_handler = logging.StreamHandler()

        formatter = logging.Formatter('%(levelname)s %(message)s', datefmt=datefmt)
        stream_handler.setFormatter(formatter)
        logging.getLogger().addHandler(stream_handler)
