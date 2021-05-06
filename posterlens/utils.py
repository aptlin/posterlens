# Copyright (c) 2021 Sasha Aptlin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import hashlib
import logging
import os
from pathlib import Path
from typing import Union
from urllib.parse import urlparse
import time
import requests
from tqdm import tqdm


def md5(fname: Union[str, Path]):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        hash_md5.update(f.read())
    return hash_md5.hexdigest()


def download(url: str, file_path: Union[str, Path], attempts=2, show_progress=False):
    """Downloads a URL content into a file (with large file support by streaming)

    :param url: URL to download
    :param file_path: Local file name to contain the data downloaded
    :param attempts: Number of attempts
    :return: New file path. Empty string if the download failed
    """
    if not file_path:
        file_path = os.path.realpath(os.path.basename(url))
    logging.info(f"Downloading {url} content to {file_path}")
    url_sections = urlparse(url)
    if not url_sections.scheme:
        logging.debug("The given url is missing a scheme. Adding http scheme")
        url = f"http://{url}"
        logging.debug(f"New url: {url}")
    for attempt in range(1, attempts + 1):
        try:
            if attempt > 1:
                time.sleep(10)  # 10 seconds wait time between downloads
            with requests.get(url, stream=True, allow_redirects=True) as response:
                response.raise_for_status()
                total_size = int(response.headers.get("content-length", 0))
                if show_progress:
                    pbar = tqdm(total=total_size, unit="MB", unit_scale=True)
                with open(file_path, "wb") as out_file:
                    for chunk in response.iter_content(
                        chunk_size=1024 * 1024
                    ):  # 1MB chunks
                        if show_progress:
                            pbar.update(len(chunk))
                        out_file.write(chunk)
                logging.info("Download finished successfully")
                return file_path
        except Exception as ex:
            logging.error(f"Attempt #{attempt} failed with error: {ex}")
