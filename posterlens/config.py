# Copyright (c) 2021 Sasha Aptlin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from dataclasses import dataclass
import logging
from multiprocessing import cpu_count


@dataclass
class Config:
    DATA_DIR: str = "data"
    IMAGE_DIR: str = "posterlens-25m/covers"
    EMBEDDING_DIR: str = "posterlens-25m/embeddings"
    DOWNLOAD_ATTEMPTS: int = 2
    MOVIELENS_25M_CHECKSUM_FN: str = "ml-25m.zip.md5"
    MOVIELENS_25M_CHECKSUM_URL: str = (
        "http://files.grouplens.org/datasets/movielens/ml-25m.zip.md5"
    )
    MOVIELENS_25M_FN: str = "ml-25m.zip"
    MOVIELENS_25M_LINKS_FN: str = "ml-25m/links.csv"
    MOVIELENS_25M_URL: str = "http://files.grouplens.org/datasets/movielens/ml-25m.zip"
    TARGET_HEIGHT: int = 512
    POOL_WORKERS: int = cpu_count() * 2

    def __init__(self):
        logging.basicConfig(level=logging.WARN)
