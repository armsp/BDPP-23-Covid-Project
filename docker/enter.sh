#! /bin/bash

# find absolute path of the directory of this script
parent_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd -P)"

# path to the repository root
repo_root="$parent_dir/.."

image_name="bdpp_covid_checkpoint"
container_name="bdpp_covid_container"

# check if the container is not already running
if [ ! "$( docker ps | grep $container_name )" ]; then

	echo "launching..."
	# launch container and bind mount the work directory for development
	docker run \
		--name $container_name \
		-it \
		-p 8080:8080 \
		-p 8888:8888 \
		-v "$repo_root/work:/work" \
		-w /work \
		--memory=8g \
		--memory-swap=20g \
		$image_name /bin/bash

	echo "saving state..."
	docker commit $container_name $image_name

	echo "cleaning up..."
	docker container rm $container_name

elif [ $1 == "new" ]; then

	echo "launching a new shell on existing container $container_name"
	docker exec -it $container_name /bin/bash
else

	echo "attaching to running process on $container_name"

	# print some context
	docker logs --tail 100 $container_name

	# attach to existing container
	docker attach $container_name
fi
