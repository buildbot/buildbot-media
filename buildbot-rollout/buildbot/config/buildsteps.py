from buildbot.process.factory import BuildFactory
from buildbot.steps.python import PyLint
from buildbot.steps.shell import ShellCommand
from buildbot.steps.source.git import Git



def get_buildsteps(working_dir):
    build_steps = BuildFactory()

    repo = Git(repourl="https://github.com/mlakewood/Buildbot-rollout.git", branch='master')

    virt_env = working_dir + '/virt/lib'

    slave_python = working_dir + '/virt/bin/python'

    env = {"LD_LIBRARY_PATH": virt_env}

    build_steps.addStep(repo)

    # # Remove the Virtual Environment from the last run
    # command = "rm -Rf %s/virt" % (working_dir)
    # build_steps.addStep(ShellCommand(workdir=working_dir, description="Clear Virtualenv", command=command.split(" ")))

    # # Create the virtual environment for the build
    # command = "virtualenv virt" 
    # build_steps.addStep(ShellCommand(workdir=working_dir, description="Create Virtualenv", command=command.split(" ")))

    # # Pip install the python packages from requirements.txt
    # command = '%s/virt/bin/pip install -r requirements.txt' % working_dir
    # build_steps.addStep(ShellCommand(workdir=working_dir, description="Install packages", command=command.split(" ")))

    # Run the tests through coverage to get test coverage at the same time
    command = "../virt/bin/coverage run --include=src -m unittest discover -vf tests"
    build_steps.addStep(ShellCommand(workdir=working_dir + '/rollout', description="rollout Unit Tests", command=command.split(" ")))

    # Output the coverage report
    command= "virt/bin/coverage report --omit=*tests* -m"
    build_steps.addStep(ShellCommand(workdir=working_dir, description="API Unit Test Coverage Report", command=command.split(" ")))

    # Run pylint. P
    command = "%s pylint %s/api --rcfile=.pylintrc" % (slave_python, working_dir)
    build_steps.addStep(PyLint(workdir=working_dir, description="API pylint", command=command.split(" ")))

    command = "./jslint js nohilite"
    build_steps.addStep(ShellCommand(workdir=working_dir + 'js', description="Insight JSLint code", command=command.split(" "))) 

    return build_steps

