#! /bin/bash

# find absolute path of the directory of this script
parent_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")"; pwd -P)"

image_name="bdpp_covid_checkpoint"

cd "$parent_dir" && docker build -t $image_name -f "$parent_dir/Dockerfile" .