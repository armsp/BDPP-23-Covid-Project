# Project
## Setup

We assume you have `pipenv` and `python 3.9` installed on your machine (or [virtual machine](../../docker/readme.md)).

1. Navigate to `project` 
2. Run `PIPENV_VENV_IN_PROJECT=1 pipenv install` This way, the virtual enviroment is created in the repository and is gone once you delete it. **If using Docker** or you know better, just run `pipenv install`.
3. Enter the virtual enviroment by `pipenv shell`
4. To launch jupyter lab, run `jupyter-lab -y --NotebookApp.token='' --ip='*' --port=8888 --allow-root`. Most of these keyword arguments are required to run smoothly in docker, so if you know better, you might get away without all of them.
6. If not already, open `localhost:8888` for jupyter lab.

## Server

In a second pipenv shell, run `is_server=1 watchmedo auto-restart -p "server.py" -R python3 -- server.py` for an autoreloading server (think nodemon).

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

## Unrelated IP

The code is backed by a computation graph system (aka `./node.py` system) that employs a fully automated smart caching scheme (`./cache.py`) for intermediate results. This system is hungry on disk space, so cleaning old results in the `./node_cache` directory may be necessary once in a while. Check disk space availability with `du -h . | sort -h`. For development, a hybrid notebook/python file system is employed via `./writefile2.py`, which simplifies combining notebooks with each other and with other python code. To reload development modules at (interactive) runtime without restarting the kernel `./require.py` is used to automatically determine the necessity of reloading another imported (or `require`'d) module. To ensure consistency and provide minimal documentation across cumputation stages, `./typesystem.py` and `./typed.py` ensure simple definition and checking of result types, respectively. This last feature is not used on the application level in this project.

### TODO

- [x] display prediction progress
- [x] introduce alternative model (plain old window regression)
- [x] ditch hospitalization rate: not enough countries covered (find a way to switch back and forth)
- [x] write: documentation for each file, especially the require, nodes, etc. lot
- [x] train on many more countries and regions
- [ ] add forward prediction scheme to ensemble
- [ ] introduce model evaluation during training using cross validation
- [ ] introduce confidence
- [ ] write: why linear model is not robust against low-evidence data
- [x] normalize threshold for automatic prediction range
- [ ] write: how to use the app
- [ ] write: why ditch hospitalization data

#### unrelated IP todo

- [ ] self-managed .gitignore for nodes (if cached nodes are small enough)
- [ ] node visualization tool
- [ ] node cache cleaning tool