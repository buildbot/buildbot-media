

####### BUILDSLAVES

# The 'slaves' list defines the set of recognized buildslaves. Each element is
# a BuildSlave object, specifying a unique slave name and password.  The same
# slave name and password must be configured on the slave.




from buildbot.buildslave import BuildSlave

def get_slaves():
    return [BuildSlave("slave", "pass")]

