We assume you have `pipenv` and `python 3.9` installed on your machine (or virtual machine).

1. Navigate to `session4` 
2. Run `PIPENV_VENV_IN_PROJECT=1 pipenv install` This way, the virtual enviroment is created in the repository and is gone once you delete it. **If using Docker** or you know better, just run `pipenv install`.
3. Enter the virtual enviroment by `pipenv shell`
4. Trust the notebook: `jupyter trust dash_app_task_with_solutions.ipynb`
5. To test the notebook of session 4, run `jupyter notebook -y --NotebookApp.token='' --ip='*' --port=8888 --allow-root`. Most of these keyword arguments are required to run smoothly in docker, so if you know better, you might get away without all of them.
6. If not already, open `localhost:8888` for jupyter.
7. Follow the steps of the notebook
