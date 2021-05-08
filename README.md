# PosterLens 25M

## Full-size posters of movies from MovieLens 25M

[MovieLens 25M](https://grouplens.org/datasets/movielens/25m/) contains 25M ratings and 1M tag applications applied to 62k+ movies by 162k users.

[PosterLens 25M](https://www.kaggle.com/aptlin/posterlens-25m) collects 62061 posters for movies from MovieLens 25 together with their ResNet-34 embeddings

This repo contains the reproducible pipeline generating the dataset.

## Download from Kaggle

Download a copy from Kaggle:

```
kaggle datasets download -d aptlin/posterlens-25m
```

## Manual data generation

0. Pick the size of a dataset from [the official page with MovieLens datasets](https://grouplens.org/datasets/movielens/) (at the moment only 25m and 20m are supported)

   ```bash
   export MOVIELENS_SIZE= <Your string>
   ```

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
   ./run.sh $MOVIELENS_SIZE
   ```

## Citation

Please cite the dataset in case you find it helpful for your research:

```
Sasha Aptlin, “PosterLens 25M.” Kaggle, 2021, doi: 10.34740/KAGGLE/DS/1321802.
```
