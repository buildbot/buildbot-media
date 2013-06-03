####### CHANGESOURCES

# the 'change_source' setting tells the buildmaster how it should find out
# about source code changes.  Here we point to the buildbot clone of pyflakes.

#from buildbot.changes.gitpoller import GitPoller
#c['change_source'] = GitPoller(
#        'git://github.com/buildbot/pyflakes.git',
#        workdir='gitpoller-workdir', branch='master',
#        pollinterval=300)

from buildbot.changes.svnpoller import SVNPoller

def get_source():
    return GitPoller

def split_file_branches(path):
    print path
    pieces = path.split('/')
    if len(pieces) > 1 and pieces[0] == 'trunk':
        return ('trunk', '/'.join(pieces[1:]))
    elif len(pieces) > 2 and pieces[0] == 'branch':
        print "found branch!"
        return ('/'.join(pieces[0:2]),
                '/'.join(pieces[2:]))
    else:
        return None
