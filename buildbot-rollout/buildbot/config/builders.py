####### BUILDERS

# The 'builders' list defines the Builders, which tell Buildbot how to perform a build:
# what steps, and which slaves can execute them.  Note that any particular build will
# only take place on one slave.


from buildbot.config import BuilderConfig
from . import buildsteps


def get_builders(name, build_dir):
    builders = []

    builders.append(
        BuilderConfig(name="12.04-" + name,
          slavenames=['slave'], slavebuilddir=build_dir,
          factory=buildsteps.get_buildsteps(build_dir + "/build")))
    
    builders.append(
        BuilderConfig(name="12.04-" + name + '_try',
          slavenames=['slave'], slavebuilddir=build_dir,
          factory=buildsteps.get_buildsteps(build_dir + "/build")))

    builders.append(
        BuilderConfig(name="12.04-" + name + '_sprint',
          slavenames=['slave'], slavebuilddir=build_dir,
          factory=buildsteps.get_buildsteps(build_dir + "/build")))


    return builders
