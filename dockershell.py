import argparse
import sys
import os
import uuid
from pprint import pprint
from os import environ
from os.path import basename, split
from subprocess import DEVNULL, run, Popen, PIPE



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('container_name', type=str)
    parser.add_argument('image_name', type=str)
    parser.add_argument('image_version', type=str)
    parser.add_argument('num_gpus', type=int)
    parser.add_argument('num_runs', type=int)

    args = parser.parse_args()

    return args


def grab_path(list):
    if len(list) == 1:
        return list[0]
    return os.path.split(list[0])[0]


def container_exists(container_name):
    inspect_proc = run(f"nvidia-docker container inspect " + container_name, shell=True, \
                       stderr=DEVNULL, stdout=DEVNULL, encoding="UTF-8")
    return not bool(inspect_proc.returncode)


def bind_mount(src, dst):
    return f"""  -v "{src}:{dst}" \\\n"""


def get_nvidia_docker_cmd(args, gpu):
    cmd = f"nvidia-docker run -d --rm --name " + args.container_name + "_" + str(uuid.uuid1()) + "\\\n"
    cmd += f"  -e CONTAINER_NAME=" + args.container_name + " \\\n"
    cmd += "-e  CUDA_VISIBLE_DEVICES=" + str(gpu) + " \\\n"
    cmd += f"  --mount type=bind,dst=/etc/machine-id,src=/etc/machine-id,readonly \\\n"
    cmd += f"  --network host --ipc host --privileged --ulimit memlock=-1 --ulimit stack=67108864 \\\n"
    cmd += f"  {environ['USER']}/{args.image_name}:{args.image_version} \n"
    return cmd

def run_cmd(cmd):
    print(f"Running: {cmd}")
    p = Popen(cmd,
             stdout=PIPE,
             stderr=PIPE,
             shell=True)
             # stdin=PIPE, #some nvidia-docker cmds are being run -it, which this would break
             # TODO: Setup nvidia-docker to not run interactively anymore

    (out, err) = p.communicate()
    print(err.decode(), end=" ")
    print(out.decode(), end=" ")
    return p


def main(args):

    for i in range(args.num_runs):
        if container_exists(args.container_name):
            pprint(f"Container named {args.container_name} already exists.  To remove existing container:")
            pprint(f"\tnvidia-docker container rm {args.container_name}")
            sys.exit(1)
        cmd_str = get_nvidia_docker_cmd(args, int(i % args.num_gpus))
        print("#!/bin/bash")
        print(cmd_str)
        p = run_cmd(cmd_str)


if __name__ == "__main__":
    args = parse_args()
    main(args)


