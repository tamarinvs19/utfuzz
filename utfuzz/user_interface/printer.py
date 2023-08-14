import logging

import tqdm


def my_print(text: str):
    logging.info(text)
    tqdm.tqdm.write(text)
