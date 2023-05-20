You can use your own `pipenv` for this project. If you prefer Docker, you can use it as a virtual machine for this project.
We assume you have `bash` installed. If not, you can also execute these steps manually with some Docker knowledge.

1. Build the Dockerfile locally by running `build.sh`. This step has only has to be done if the `Dockerfile` changes. We do not use Docker's layer caching, because we want the container to keep it's state as an image.
2. Enter the container using `enter.sh`. Make sure you exit the container properly with `ctrl-d`, otherwise the image state will not be saved. This will not result in lost progress, but you may have to wait for `pipenv` to reinstall some things next time you enter it.
