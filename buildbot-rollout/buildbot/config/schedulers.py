####### SCHEDULERS

# Configure the Schedulers, which decide how to react to incoming changes.  In this
# case, just kick off a 'runtests' build

#from buildbot.schedulers.timed import Periodic
#c['schedulers'] = []
#c['schedulers'].append(SingleBranchScheduler(
#                            name="all",
#                            branch='master',
#                            treeStableTimer=None,
#                            builderNames=["runtests"]))

#print c

#periodic = Periodic("every_6_hours", ['slave'], 6*60*60)
#c['schedulers'] = [periodic]

from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.schedulers.timed import Periodic
from buildbot.schedulers.trysched import Try_Jobdir
from buildbot.schedulers.trysched import Try_Userpass


def get_schedulers(build):

    quick = SingleBranchScheduler(name='quick',
                                branch='master',
                                treeStableTimer=60,
                                builderNames=["12.04-" + build])

    sprint = SingleBranchScheduler(name='sprint',
                                branch='sprint',
                                treeStableTimer=60,
                                builderNames=["12.04-" + build + '_sprint'])

    try_job = Try_Jobdir(name="try_job",
                    builderNames=["12.04-" + build + '_try'],
		    jobdir="jobdir")


    return [quick, sprint, try_job]
