from buildbot.process.factory import BuildFactory
from buildbot.steps.python import PyLint
from buildbot.steps import source, shell



def get_buildsteps(working_dir):
    build_steps = BuildFactory()

    repo = source.SVN(baseURL='http://subversion_server/subversion/rollout/', defaultBranch='trunk/', workdir=working_dir, username='markl', password='password')

    virt_env = working_dir + '/virt/lib'

    slave_python = working_dir + '/virt/bin/python'

    env = {"LD_LIBRARY_PATH": virt_env}

    build_steps.addStep(repo)

    command = "rm -Rf %s/virt" % (working_dir)
    build_steps.addStep(shell.ShellCommand(workdir=working_dir, description="Clear Virtualenv", command=command.split(" ")))

    command = "virtualenv virt" 
    build_steps.addStep(shell.ShellCommand(workdir=working_dir, description="Create Virtualenv", command=command.split(" ")))

    command = 'pip install -r requirements.txt'
    build_steps.addStep(shell.ShellCommand(workdir=working_dir, description="Install packages", command=command.split(" ")))

    command = "virt/bin/coverage run --include=api/* --omit=*.json python -m unittest discover -vf"
    build_steps.addStep(shell.ShellCommand(workdir=working_dir, description="rollout Unit Tests", command=command.split(" "), env=env))

    command= "virt/bin/coverage report --omit=*tests* -m"
    build_steps.addStep(shell.ShellCommand(workdir=working_dir, description="API Unit Test Coverage Report", command=command.split(" ")))

    command = "%s sws_pylint.py %s/api --rcfile=.pylintrc" % (slave_python, working_dir)
    build_steps.addStep(PyLint(workdir=working_dir, description="API pylint", command=command.split(" ")))

    command = "./jslint js nohilite"
    build_steps.addStep(shell.ShellCommand(workdir=working_dir + '/front_ends/insight', description="Insight JSLint code", command=command.split(" "))) 

    return f

