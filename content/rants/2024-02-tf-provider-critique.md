+++
title = "Critique of the entry level barrier for writing a Terraform provider"
date = 2024-02-29
+++

Context: recently a need for managing Jira with Terraform emerged, mainly for
[IAM][1] purposes at **work** (god I tell you how much easier it is to
administer access through text). However there's only [one provider][2] for it
and tbh it kinda sucks - it's outdated and the maintainer has only tested it for
a Jira instance, not the Jira Cloud platform we use.

So I decided to write my first TF ~~provider~~ plugin _is what they call it now_,
like any sane person would 🙄. I am also new to Go so it [doubles the fun][3].

The two APIs for Jira Instance and Jira Cloud differ slightly so I decided
to start from scratch instead of forking the repo. Hashicorp kindly provides a
template repo on GitHub to get you started.  
That repo is shit. It is full of bloat and has like 20 tools for just the
release process.  
Maybe that's the standard for Go these days idk..

Following [the guide][4] and replicating it

<!-- TODO: shorten this... -->


[1]: https://en.wikipedia.org/wiki/Identity_management
[2]: https://github.com/fourplusone/terraform-provider-jira/issues
[3]: https://www.youtube.com/watch?v=8RtGlWmXGhA
<!-- more -->
