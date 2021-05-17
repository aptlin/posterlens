# Copyright (c) 2021 Sasha Aptlin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import csv
import logging
import random
import zipfile
from functools import cached_property
from io import TextIOWrapper
from multiprocessing import Pool, Value
from pathlib import Path
from time import sleep

import requests
from imdb import IMDb
import torch
from tqdm import tqdm
from img2vec_pytorch import Img2Vec
from PIL import Image, ImageFile
import numpy as np

from posterlens.config import Config
from posterlens.field import Field
from posterlens.utils import download, md5

Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True


class PosterLens:
    def __init__(
        self, size: str = "25m"  # only 20m and 25m are supported at the moment
    ):
        self.config = Config()
        self.field = Field()
        self.img2vec = Img2Vec(cuda=torch.cuda.is_available(), model="resnet34")
        self.size = size.lower()

    @cached_property
    def data_dir(self):
        data_dir = Path(self.config.DATA_DIR)
        data_dir.mkdir(exist_ok=True, parents=True)
        return data_dir

    @cached_property
    def image_dir(self):
        image_dir = self.data_dir / self.config.IMAGE_DIR_TEMPLATE.format(self.size)
        image_dir.mkdir(exist_ok=True, parents=True)
        return image_dir

    @cached_property
    def embedding_dir(self):
        embedding_dir = self.data_dir / self.config.EMBEDDING_DIR_TEMPLATE.format(
            self.size
        )
        embedding_dir.mkdir(exist_ok=True, parents=True)
        return embedding_dir

    @cached_property
    def data_fn(self):
        return self.data_dir / (
            self.config.MOVIELENS_PREFIX_TEMPLATE.format(self.size) + ".zip"
        )

    @cached_property
    def movies_fn(self):
        return self.config.MOVIELENS_MOVIES_FN_TEMPLATE.format(
            self.size, "dat" if self.size in (self.config.SIZE_1M) else "csv"
        )

    @cached_property
    def data_url(self):
        return self.config.MOVIELENS_ZIP_URL_TEMPLATE.format(self.size)

    @cached_property
    def checksum_url(self):
        return self.config.MOVIELENS_CHECKSUM_URL_TEMPLATE.format(self.size)

    def collect(self):
        self._download_primary_data()
        self._download_covers()
        self._generate_embeddings()

    def _download_primary_data(self):
        with requests.get(
            self.checksum_url,
            allow_redirects=True,
        ) as response:
            response.raise_for_status()
            checksum_data = response.content.decode("utf-8")
            if self.size == self.config.SIZE_25M:
                checksum = checksum_data.split()[0].strip()
            elif self.size in (self.config.SIZE_20M, self.config.SIZE_1M):
                checksum = checksum_data.split("=")[1].strip()
            else:
                raise ValueError("Unsupported size")

        if not self.data_fn.exists():
            logging.info(f"Downloading the dataset to {self.data_fn}...")
            download(self.data_url, self.data_fn, show_progress=True)

        test_checksum = md5(self.data_fn)
        if test_checksum != checksum:
            logging.warn(f"The dataset at {self.data_fn} is corrupted, overwriting...")
            self.data_fn.unlink()
            download(self.data_url, self.data_fn, show_progress=True)

    def _download_image(self, row):
        movie_id = row[self.field.movie_id]
        title = row[self.field.title]
        target_image_fn = self.image_dir / f"{movie_id}.jpg"
        if not target_image_fn.exists():
            try:
                imdb = IMDb(accessSystem="http", reraiseExceptions=True, timeout=False)
                movie = imdb.search_movie(title)[0]
                cover_url = movie.get("full-size cover url", "").strip()
                if cover_url:
                    sleep(random.randint(3, 5))
                    download(cover_url, target_image_fn, 1)
                    return 0
                else:
                    raise ValueError(f"No cover for the movie {movie_id}")
            except Exception as err:
                logging.info(f"Failed to get movie #{movie_id} details: {str(err)}")
                return 1
        else:
            return 0

    def _parse_1m(self, f):
        fieldnames = [
            self.field.movie_id,
            self.field.title,
            self.field.genres,
        ]
        for line in f:
            parsed = line.decode("latin-1").split("::")
            yield dict(zip(fieldnames, parsed))

    def _download_covers(self):
        with zipfile.ZipFile(self.data_fn, "r") as archive:
            movie_count = 0
            with archive.open(self.movies_fn, "r") as f:
                for _ in f:
                    movie_count += 1

            with archive.open(self.movies_fn, "r") as f:

                if self.size in (self.config.SIZE_1M):
                    reader = self._parse_1m(f)
                else:
                    reader = csv.DictReader(
                        TextIOWrapper(f, "utf-8"),
                        delimiter=",",
                    )

                with Pool(self.config.POOL_WORKERS) as pool:
                    with tqdm(
                        total=movie_count, unit="covers", desc="Downloading covers"
                    ) as pbar:
                        total = 0
                        for res in pool.imap_unordered(self._download_image, reader):
                            pbar.update()
                            total += res

                        logging.warn(f"Missing covers for {total} movies.")

    def _generate_embedding(self, fn: Path):
        if any(str(fn).endswith(ext) for ext in ("jpg", "png")):
            img = Image.open(fn).convert("RGB")
            vec = self.img2vec.get_vec(img)
            np.save(self.embedding_dir / f"{fn.stem}.npy", vec)
        else:
            logging.warn(f"Skipping {fn}")

    def _generate_embeddings(self):
        total = sum(1 for _ in self.image_dir.iterdir())
        with Pool(self.config.POOL_WORKERS) as pool:
            with tqdm(
                total=total, unit="covers", desc="Running embedding inference"
            ) as pbar:
                for _ in pool.imap_unordered(
                    self._generate_embedding, self.image_dir.iterdir()
                ):
                    pbar.update()
