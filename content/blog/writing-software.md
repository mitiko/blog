+++
title = "Writing software from the bottom up"
date = 2023-03-21
+++

Writing software has become an industry.
When something becomes an industry, more and more money gets involved,
subsequently more and more people.
With more people come, more more organizational problems.

> [Conway's law](https://en.wikipedia.org/wiki/Conway%27s_law)
> Software is bound to repeat the structure that the organizations that wrote
> it uses for internal communication.

Mainly, we're shitting capitalism in the perfectly structured world of
computers.

Most of the work can be scoped to specific groups (like database operations,
application, sales, etc) which then become organizational scopes of people -
teams.

Mandatory meetings are like mandatory server communication. If they have nothing
to say, that's all a meeting was - wasted TCP packets (/ CPU cycles?).

<!-- My experience working with other companies and trying to reach somebody who is
competent enough to answer my questions about the general design and structure
of their systems. -->

So, each next level of team abstraction cares even less about the actual code
running on the machines. The sales person doesn't care about CVE-(todo some sample cve id).
They care about being "secure". They don't care that there's a buffer overflow
exploitable if you breach the firewall, they only care what publicity it will
generate.

That's because each level of abstraction cares about a slightly different scope
of the ~~end product~~ (project?).

At the lowest level, it's the servers apologizing for your shit code every
nanosecond of every day of every month for the rest of its lifespan.
<!-- Silicon valley reference -->
The coders care about the code.
They care about performance, they care about it "working".

Their team leaders about code readability, reusability, maintainability.
They've stayed longer at the company and they can't afford to have you write
shit java in the legacy shitdump of bytecode.

Their managers care about "meeting deadlines".
Where the deadlines are imposed by some even less knowledgable sales people.

They care about the money.

A factor up, still caring about the money but in long-term is the CTO, COO, CEO, etc.

But at the end of the day it doesn't really matter how much shit code you write,
it's not a factor in whether you'd get replaced by 4 uknowledgable interns that
each get a fifth of your salary. It doesn't matter if your code is reusable if
Susan is going to force push her changes to the repo.
everybody gets paid money. So we all care about the money.
If everybody's incentive is in a different direction, then your product will
become as good as the will outside of money of people.
You could argue all the actual truly meaningful work was done for free, and
you pay for the bullshit.

My point is.
Maybe we should all unite on a "ideas" level.
Or maybe that's just the next bullshit scope, that the ceo probably tried to
push you in anyways.

Perhaps a better title for this is
- the shitshow of writing software
- preparation for the world of software
- idk


