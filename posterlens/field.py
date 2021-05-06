# Copyright (c) 2021 Sasha Aptlin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from dataclasses import dataclass


@dataclass
class Field:
    movie_id: str = "movieId"
    imdb_id: str = "imdbId"
    tmdb_id: str = "tmdbId"
