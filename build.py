import argparse
import os
import shlex
import shutil
import subprocess

def run_cmd(cmd):
    p = subprocess.Popen(shlex.split(cmd), shell=True)
    p.wait()

parser = argparse.ArgumentParser()

parser.add_argument("--generator", type=str, default="", help="CMake generator")

parser.add_argument("--variant", type=str, default="RelWithDebInfo", help="CMake build variant")

parser.add_argument("--cmake-vars", type=str, nargs="*", default=[], help="CMake options and variables")

parser.add_argument("--steps", type=str, nargs="*", default=['clean','configure','build'], help="Build steps to run")

parser.add_argument("--graphviz-file", type=str, default="", help="Graphviz output file")

args = parser.parse_args()

dolphin_dir = "./dolphin"
source_dir = dolphin_dir
build_dir = dolphin_dir + "/Build"
binary_dir = dolphin_dir + "/Binary"

if 'clean' in args.steps:
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    if os.path.exists(binary_dir):
        shutil.rmtree(binary_dir)

if 'configure' in args.steps:
    run_cmd("cmake -S {source_dir} -B {build_dir} "
            "-G {generator} "
            "-DCMAKE_BUILD_TYPE={variant} "
            "{cmake_args} "
            "{graphviz_arg} "
            .format(source_dir=source_dir, build_dir=build_dir,
                    generator="\"{}\"".format((args.generator or "")),
                    variant=args.variant,
                    cmake_args=" ".join(["-D" + var for var in args.cmake_vars]),
                    graphviz_arg="--graphviz={}".format(args.graphviz_file) if args.graphviz_file else ""))

if 'build' in args.steps:
    run_cmd("cmake --build {build_dir} "
            "--config {variant} "
            "--target dolphin-emu "
            .format(build_dir=build_dir,
                    variant=args.variant))
