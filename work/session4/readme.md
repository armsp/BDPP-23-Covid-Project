We assume you have `pipenv` and `python3` installed on your machine.

1. Navigate to `session4` 
2. Run `PIPENV_VENV_IN_PROJECT=1 pipenv install` This way, the virtual enviroment is created in the repository and is gone once you delete it. **If using Docker** or you know better, just run `pipenv install`.
3. Enter the virtual enviroment by `pipenv shell`
4. Trust the notebook: `jupyter trust dash_app_task_with_solutions.ipynb`
5. To test the notebook of session 4, run `jupyter notebook -y --NotebookApp.token='' --ip='*' --port=8888 --allow-root`
