 
if [ "$3" == "" ] ; then
   echo "usage: dockershell <image_name> <version> <container_name>"
   echo Example:
   echo dockershell cpsc392_server_test latest mytest
   exit 1
fi

image=$1
version=$2
name=$3
gpu=$4

nvidia-docker container inspect ${name} 1>/dev/null 2>&1
if [ $? -ne 0 ] ; then
  echo "Creating new container ${name}..."
  nvidia-docker run -d --rm --name ${name} \
        --user $(id -u):$(id -g) -e DISPLAY=$DISPLAY -e CONTAINER_NAME=${name} -e  CUDA_VISIBLE_DEVICES={$GPU}\
        --network host --ipc host --ulimit memlock=-1 --ulimit stack=67108864 --privileged \
        ${USER}/${image}:${version} 
else
  echo "Container named '${name}' already exists.  To remove existing container:"
  echo "   nvidia-docker container rm ${name}"
fi

#TODO add GPUs



