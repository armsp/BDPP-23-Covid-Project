We assume you have `pipenv` and `python 3.9` installed on your machine (or virtual machine).

1. Navigate to `project` 
2. Run `PIPENV_VENV_IN_PROJECT=1 pipenv install` This way, the virtual enviroment is created in the repository and is gone once you delete it. **If using Docker** or you know better, just run `pipenv install`.
3. Enter the virtual enviroment by `pipenv shell`
4. To launch jupyter lab, run `jupyter-lab -y --NotebookApp.token='' --ip='*' --port=8888 --allow-root`. Most of these keyword arguments are required to run smoothly in docker, so if you know better, you might get away without all of them.
6. If not already, open `localhost:8888` for jupyter lab.
