# Project
## Setup

We assume you have `pipenv` and `python 3.9` installed on your machine (or [virtual machine](../../docker/readme.md)).

1. Navigate to `project` 
2. Run `PIPENV_VENV_IN_PROJECT=1 pipenv install` This way, the virtual enviroment is created in the repository and is gone once you delete it. **If using Docker** or you know better, just run `pipenv install`.
3. Enter the virtual enviroment by `pipenv shell`
4. To launch jupyter lab, run `jupyter-lab -y --NotebookApp.token='' --ip='*' --port=8888 --allow-root`. Most of these keyword arguments are required to run smoothly in docker, so if you know better, you might get away without all of them.
6. If not already, open `localhost:8888` for jupyter lab.

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