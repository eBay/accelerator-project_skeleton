#!/usr/bin/env python3
#
# This takes a stab at initialising your setup in a reasonable
# way for quick testing. You should modify it to suit your project.
#
# You need to have the following packages (Debian names) installed:
# build-essential python-dev python3-dev zlib1g-dev git virtualenv

from subprocess import check_call
from os.path import exists, abspath, join
from os import makedirs, getenv, unlink
from sys import exit
from multiprocessing import cpu_count

if exists("accelerator/daemon.py"):
	print("Appears to already be initialized")
	exit(1)

versions = []
for v in (2, 3):
	path = join(abspath("venv"), "py%d" % (v,))
	python = "python%d" % (v,)
	check_call(["virtualenv", "-p", python, path])
	check_call([join(path, "bin/pip"), "install", "-r", "venv/requirements.py%d.txt" % (v,)])
	print()
	print("Running gzutil tests")
	check_call([join(path, "bin/python"), join(path, "src/gzutil/test.py")])
	try:
		unlink("_tmp_test.gz")
	except OSError:
		pass
	print()
	versions.append("py%d=%s/bin/python\n" % (v, path,))

accel_home = join(getenv("HOME"), "accelerator")
for dn in ("conf", join(accel_home, "results"), join(accel_home, "workdirs/TEST"),):
	makedirs(dn, exist_ok=True)

CONF="""# var=value, value can have ${VAR=DEFAULT} to import env vars.

# workdir=NAME:PATH:SLICES
# You can have as many workdir lines as you want
workdir=TEST:${HOME}/accelerator/workdirs/TEST:%d

# You can only have one target workdir.
# All built jobs end up there.
target_workdir=TEST

# List all other workdirs you want to import here (comma separated)
source_workdirs=TEST

# Methods are imported from these directories (comma separated)
method_directories=dev,standard_methods,example1,example_perf

# automata scripts save things here
result_directory=${HOME}/accelerator/results

# import methods look under here
source_directory=/some/other/path

logfilename=${HOME}/accelerator/daemon.log
hash_override=<hash_check_override>

# python versions to use
# (the left side here is what you put on the right side in methods.conf)
"""

slices = max(cpu_count() - 1, 1)
with open("conf/framework.conf", "w", encoding="utf-8") as fh:
	fh.write(CONF % (slices,))
	fh.write("".join(versions))

check_call(["git", "submodule", "init"])
check_call(["git", "submodule", "update"])

print("""
All done!

You should consider whether you want conf/framework.conf in your repository,
and remove it from .gitignore if you do.
""")
