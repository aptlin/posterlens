# PosterLens 25M

[MovieLens 25M](https://grouplens.org/datasets/movielens/25m/) contains 25 million ratings and one million tag applications applied to 62k+ movies by 162,000 users.

[PosterLens 25M](https://github.com/aptlin/posterlens) collects 62061 posters for movies from MovieLens 25 together with their ResNet-34 embeddings

This repo contains the reproducible pipeline generating the dataset.

## Setup

1. Clone the repo:
   ```bash
   git clone git@github.com:aptlin/posterlens.git
   ```
2. Install dependencies using [poetry](https://github.com/python-poetry/poetry):
   ```
   cd posterlens
   poetry install
   ```

3. Run the pipeline:
    ```
    ./run.sh
    ```

## Citation

Please cite the dataset in case you find it helpful for your research:

```
Sasha Aptlin, “PosterLens 25M.” Kaggle, 2021, doi: 10.34740/KAGGLE/DS/1321802.
```
