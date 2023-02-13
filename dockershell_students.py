import argparse
import sys
import os
import uuid
import yaml
from pprint import pprint
from os import environ
from os.path import basename, split
from subprocess import DEVNULL, run, Popen, PIPE

from tensorflow.python.client import device_lib

def read_yaml(fpath_yaml):
    yml_conf = None
    with open(fpath_yaml) as f_yaml:
        yml_conf = yaml.load(f_yaml, Loader=yaml.FullLoader)
    return 

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--yaml", help="YAML file for container config.")

    args = parser.parse_args()

    return args


def container_exists(container_name):
    inspect_proc = run(f"nvidia-docker container inspect " + container_name, shell=True, \
                       stderr=DEVNULL, stdout=DEVNULL, encoding="UTF-8")
    return not bool(inspect_proc.returncode)


def bind_mount(src, dst):
    return f"""  -v "{src}:{dst}" \\\n"""


def get_available_gpus():
    local_device_protos = device_lib.list_local_devices()
    return [x.name for x in local_device_protos if x.device_type == 'GPU']

def get_nvidia_docker_cmd(config):
    cmd = f"nvidia-docker run "
    if config["interactive"]:
        cmd += "-it "
    else:
        cmd += "-d --rm -"

    container_name = config["container_name"] + "_" + str(uuid.uuid1())
    while container_exists(container_name):
            container_name = config["container_name"] + "_" + str(uuid.uuid1())

    cmd += " --name " + container_name + "\\\n"
    cmd += "  -e CONTAINER_NAME=" + config["container_name"] + " \\\n"
    cmd += "-e  CUDA_VISIBLE_DEVICES=" + str(config["gpu"]) + " \\\n"
    if config["interactive"]:
        cmd += "-e DISPLAY=$DISPLAY --entrypoint \"/bin/bash\" \\\n"
    else:
        cmd += "--entrypoint " + config["entrypoint"]
    cmd += "  --mount type=bind,dst=/etc/machine-id,src=/etc/machine-id,readonly \\\n"

    #Top level deirectory that can have subdirectories for models, input, output, code, etc.
    cmd += bind_mount(config["run_dir"], "/app/rundir/")
 
    cmd += "  --network host --ipc host --privileged --ulimit memlock=-1 --ulimit stack=67108864 \\\n"
    cmd += " " +  environ["USER"] + "/" + config["image_name"] + ":" + config["image_version"] + "\n"
    return cmd

def run_cmd(cmd):
    print(f"Running: {cmd}")
    p = Popen(cmd,
             stdout=PIPE,
             stderr=PIPE,
             shell=True)
             # stdin=PIPE, #some nvidia-docker cmds are being run -it, which this would break

    (out, err) = p.communicate()
    print(err.decode(), end=" ")
    print(out.decode(), end=" ")
    return p

def main(config):
        cmd_str = get_nvidia_docker_cmd(config)
        print("#!/bin/bash")
        print(cmd_str)
        p = run_cmd(cmd_str)

if __name__ == "__main__":
    args = parse_args()
    config = read_yaml(args.yaml)
    main(config)

