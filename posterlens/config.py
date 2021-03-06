# Copyright (c) 2021 Sasha Aptlin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from dataclasses import dataclass
import logging
from multiprocessing import cpu_count
from pathlib import Path


@dataclass
class Config:
    DATA_DIR: str = "data"
    POSTERLENS_PREFIX_TEMPLATE: str = "posterlens-{}"
    IMAGE_DIR_TEMPLATE: str = str(Path(POSTERLENS_PREFIX_TEMPLATE) / "covers")
    EMBEDDING_DIR_TEMPLATE: str = str(Path(POSTERLENS_PREFIX_TEMPLATE) / "embeddings")
    DOWNLOAD_ATTEMPTS: int = 2
    TARGET_HEIGHT: int = 512
    POOL_WORKERS: int = cpu_count() * 2

    SIZE_1M = "1m"
    SIZE_20M = "20m"
    SIZE_25M = "25m"

    MOVIELENS_PREFIX_TEMPLATE: str = "ml-{}"
    MOVIELENS_MOVIES_FN_TEMPLATE: str = str(
        Path(MOVIELENS_PREFIX_TEMPLATE) / "movies.{}"
    )
    MOVIELENS_BASE_URL: str = "http://files.grouplens.org/datasets/movielens/"
    MOVIELENS_ZIP_URL_TEMPLATE: str = (
        MOVIELENS_BASE_URL + MOVIELENS_PREFIX_TEMPLATE + ".zip"
    )
    MOVIELENS_CHECKSUM_URL_TEMPLATE: str = MOVIELENS_ZIP_URL_TEMPLATE + ".md5"

    def __init__(self):
        logging.basicConfig(level=logging.WARN)
