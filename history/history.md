(history from @warner in https://github.com/moshez/expert-twisted/pull/1)

---

(some historical notes, nothing that needs to be included)

I wrote the predecessor to Buildbot in 2000-2001, when I was working at a
router company and got tired of hassling my coworkers each morning when they'd
checked code into CVS that worked on their Solaris box but not on my Linux
machine. It was closed-source, and I used asyncore and pickle to implement an
RPC system, in which the workers drove the whole process, and the central
buildmaster only accepted status information from the workers to render it on a
web-based waterfall display. It was modelled closely Mozilla's "Tinderbox", at
least on what little I'd seen of that.

In the process of looking for examples of asyncore, I discovered Twisted, and
found that it was just like what I was writing, except a couple of years more
advanced (the first Twisted commit was in mid-2001, but Glyph and the others
had been developing the core ideas in other forms for a while before that
point).

I left that company and the code behind in 2002, and decided that a clean
reimplementation would be a good way to learn Twisted (which certainly shows in
places). The new Buildbot repo was first in CVS, then Arch until 2006, then
Darcs until 2008, when I think Dustin finally convinced us to move to Git.

I first presented it at PyCon in early 2003, and Twisted was the first
customer. A couple of other projects picked it up, and eventually Mozilla
switched over too.

There was certainly no inlineCallbacks back then. I first heard about Python
during the 2.2 cycle when the release notes mentioned generators, and I
realized that wherever this language was going, I wanted to come along. I
really liked the fact, unlike with threads, you could tell when you lost
control of the CPU because you had to return from a method: very explicit.

I was allergic to databases, not sure why, didn't have much experience with
them, so I was really into local files (and I hadn't yet outgrown Pickle at
that point, and JSON hadn't been discovered yet). I fully agree with the
problem of using synchronous calls instead of anticipating asynchronousness
from the very beginning. Back in those days, networks were slow, and disks
seemed fast, so I tended to prioritize simplicity of blocking disk writes.
There was this general idea that the only thing you might possibly wait upon
was a human, which I think is why threads were so popular (and Java not really
offering anything else didn't help).

Most of the decisions that a build process needed to make were short and could
be blocking without much problem, but over time the feature set grew: Locks, in
particular, needed some work to accomodate.

Perspective Broker: I was (and still am) into the E programming language, from
which we get Promises and RemoteReferences and several other concepts, and PB
was very much inspired by E. And I did a lot of documentation work on PB (the
other PyCon presentation I did that first year was on PB's "Translucent
References"). So I went a bit off the deep end in Buildbot, using PB for the
main RPC between workers and the buildmaster. In retrospect, some custom
protocol might have been better, at least it might have been easier to port to
other languages. This was before protobufs or JSON-RPC, and before everything
else gave up on anything other than HTTP.

(around the same time, I started Foolscap, which is a properly-encrypted form
of PB, with better/more-flexible argument serialization. I went even more
overboard on it, using Foolscap for Tahoe-LAFS, and now we're having similar
Python-lockin problems there, plus performance slowdowns because the
serialization is too flexible)

PB isn't too hard to implement in other languages, at least not as bad as
Foolscap, but it implies/imposes a particular object model, so you kind of have
to buy into that first. I think I designed Buildbot's hierarchy of "things that
worker data might be talking about" around PB objects: Builders, BuildSteps,
RemoteCommands, the various stdout/stderr/logfile channels. Each such object
has remote messages (from workers) to notify the buildmaster that the thing has
started, has spawned a new next-lower-level object, has changed status, has
finished. If we weren't using PB, then we'd probably have a bunch of messages
that each included a simple object number, and the buildmaster would have to
use a big dispatch table to figure out what to do with the new piece of status.
PB includes that dispatch table already.

---

I noticed the ".. and its position in the open source world" line, so a bit
more:

when Buildbot first came out, I think the only real other thing out there was
Tinderbox, and it had some problems that made me want something else:

*   no scheduling: workers just ran an infinite loop of (checkout, build, test, repeat). I wanted something that would leave a worker idle until something really needed to be done
*   all configuration happened on the workers: you could really only admin the thing if you could log into each worker and change things
*   the web page was the only status display, I think
*   nothing was packaged, I don't know how you would have run it anywhere outside of mozilla

I wrote the buildbot-predecessor to test cross-platform functionality of the
router code (we had different kinds of CPUs in the device, plus everything was
supposed to work on our desktop machines too), and then the second use case was
Twisted, where I wanted to make sure that it worked on a variety of platforms.
The idea was that if you had some unusual system, and you didn't know how to
test Twisted yourself, you could still contribute to the project by letting us
run those tests on your computer. So at least if something broke, we'd find out
about it immediately.

So the goals for Buildbot were to let a central admin drive everything, and the
worker admins only needed to install the software and connect it to the
buildmaster. And to make status delivery flexible enough (taking advantage of
all those protocols that Twisted supported: web, email, IRC, instant messaging)
that project members could learn about problems quickly.

I think we helped move the general concept of Continuous Integration forward
(it wasn't really called CI at that point). I think it was a couple years later
when more polished systems started coming out: CruiseControl (except it was
kinda java-centric?), and Jenkins (called something else at first), many of
which weren't open-source but were easier to configure (all web-based). I
registered buildbot.org pretty early, with the idea that we could host
buildmasters and workers for other projects, but that was way before
virtualization and containers became programmatically available, so we weren't
really ever in a position to provide the kinds of services that Travis
eventually delivered so well.

---


I left that router company in February of 2002, and I think I
started working on the new version right away. I registered the
sourceforge project on 04-feb-2003. It looks like I made the first
public presentation about Buildbot at PyCon 2003 (which would have
been in April, I think). There's a link on
https://wiki.python.org/moin/PyConDC2003/Papers to the paper
(http://www.lothar.com/tech/papers/PyCon-2003/buildbot-pycon/buildbot.html),
although it says "Buildbot is currently under development", so maybe
I hadn't made the first release yet. Twisted was using it as early
as Feb-2003.

I pulled a copy of the NEWS file from an old git commit and the
bottom of it says the first release was 0.3.1, made 29-Apr-2003 (I
was probably using baz or TLA or something really experimental back
then, and *that* repo is surely covered in mold on a dusty hard
drive in a closet somewhere, but the NEWS file got copied ovre
fairly intact).

The oldest release email I can find says that 0.3.5 ("a slightly
experimental release") was tagged on 19-Sep-2003, requring the
then-brand-new Twisted-1.0.7.

hope that helps,
 -Brian
