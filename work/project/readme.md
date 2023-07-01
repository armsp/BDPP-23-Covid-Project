# Project
## Report

Find the project report [here](./report.md).

## Setup

We assume you have `pipenv` and `python 3.9` installed on your machine (or [virtual machine](../../docker/readme.md)).

1. Navigate to `project` 
2. Run `PIPENV_VENV_IN_PROJECT=1 pipenv install` This way, the virtual enviroment is created in the repository and is gone once you delete it. **If using Docker** or you know better, just run `pipenv install`.
3. Enter the virtual enviroment by `pipenv shell`
4. To launch jupyter lab, run `jupyter-lab -y --NotebookApp.token='' --ip='*' --port=8888 --allow-root`. Most of these keyword arguments are required to run smoothly in docker, so if you know better, you might get away without all of them.
6. If not already, open `localhost:8888` for jupyter lab.

## Server / webapp

In a second pipenv shell, run `is_server=1 watchmedo auto-restart -p "server.py" -R python3 -- server.py` for an autoreloading server (think nodemon). You can launch this shell from jupyter, Visual Studio Code or by creating a new shell in terminal.

## Model installation

If you do not want to train the model(s) yourself and you have a pickled model, from this here directory (`project`) execute the model installation script: E.g. `python3 install_model.py full.pkl train_honest_forward`. Here `full.pkl` is the path to your pickled model and `train_honest_forward` is the name of the computation node that yields this model normally. Essentially, we perform a manual cache insertion to avoid computation. Warning: This may circumvent automatic cache invalidation. Make sure you know what you are doing and know where the model `full.pkl` comes from. A pretrained model of the latest version is always available [here](https://gnorpel.com/full.pkl).

## Git

Before you commit anything with git, make sure you are not committing any artifact files by editing the local `.gitignore`.

## Data

Please put all the data you require in the `data/` directory, to keep the working directory clean. For now, we have it on version control.

## Installation

Whenever you need to install packages, open up a terminal in jupyter lab and use `pipenv install ...`. This ensures that your installation is registered in git and not just on your local machine.

## Data Finder

The data finder is a collection of urls for all the different data required.

[Google Docs](https://docs.google.com/spreadsheets/d/1qD_zII1CdFMjRE_KWZzJhuWgyQHtI6_IeFByLETaPnk)

## Project Outline

The general direction we want to take in this project is outlined [here](https://docs.google.com/document/d/1nTZxaHd7YsTs8NGOBT5wBXATSmV-iW3Yf0dg_U_U9kY/edit).

## Unrelated intellectual property

For this project, ignore the following files. They are important for operations, but considered *development tools* and were not made during the scope of this project:

- `cache.py`
- `hashing.py`
- `nodes.py`
- `require.py`
- `signature_match_args.py`
- `typed.py`
- `typesystem.py`
- `writefile2.py`

The code is backed by a computation graph system (aka `./node.py` system) that employs a fully automated smart caching scheme (`./cache.py`) for intermediate results. This system is hungry on disk space, so cleaning old results in the `./node_cache` directory may be necessary once in a while. Check disk space availability with `du -h . | sort -h`. For development, a hybrid notebook/python file system is employed via `./writefile2.py`, which simplifies combining notebooks with each other and with other python code. To reload development modules at (interactive) runtime without restarting the kernel `./require.py` is used to automatically determine the necessity of reloading another imported (or `require`'d) module. To ensure consistency and provide minimal documentation across cumputation stages, `./typesystem.py` and `./typed.py` ensure simple definition and checking of result types, respectively. 

### TODO

- [x] display prediction progress
- [x] introduce alternative model (plain old window regression)
- [x] ditch hospitalization rate: not enough countries covered (find a way to switch back and forth)
- [x] write: documentation for each file, especially the require, nodes, etc. lot
- [x] train on many more countries and regions
- [x] introduce model evaluation during training using cross validation against out-of-sample time series
- [x] write: how to use the app
- [x] write: why ditch hospitalization data
- [x] write: why linear model is not robust against low-evidence data and switch to random forest
- [x] write: why evaluation of time series with r2 is difficult and arbitrary, but luckily not the entire focus
- [x] find some way to add trained models to deliverable

#### maybe / future
- [ ] introduce confidence
- [x] normalize threshold for automatic prediction range
- [ ] evaluation with balanced train/test split (estimate varies strongly with the number of WEIRD countries in test set)
- [ ] demonstrate how the honest_forward model only works in WEIRD countries (some correlation plot for GDP)

#### unrelated IP todo

- [ ] node visualization tool
- [ ] node cache cleaning tool