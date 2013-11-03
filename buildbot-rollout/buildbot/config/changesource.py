####### CHANGESOURCES

# the 'change_source' setting tells the buildmaster how it should find out
# about source code changes.  Here we point to the buildbot clone of pyflakes.

#from buildbot.changes.gitpoller import GitPoller
#c['change_source'] = GitPoller(
#        'git://github.com/buildbot/pyflakes.git',
#        workdir='gitpoller-workdir', branch='master',
#        pollinterval=300)

from buildbot.changes.gitpoller import GitPoller

def get_source():
    return GitPoller("https://github.com/mlakewood/Buildbot-rollout.git", branch="master", pollinterval=10)

