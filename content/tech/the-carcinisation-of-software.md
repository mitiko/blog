+++
title = "The Carcinisation of Software"
date = 2024-02-29
+++

Retrospective of my first year in the industry:
- the hammer principle
- self-serve principle
- how to ask good questions..
- if it is not enforced by code it will not be followed
  - any policy not enforced with code will not be respected (due to laziness, miscommunication, or out of spite)

During my first year in the tech industry (as a system enginner & architect (whatever that means)),
I had to acquaint myself with Terraform and infrastructure as code.
I played around a little bit with TF but the bulk of our work was CAF and I hated it.
Perhaps I dislike the framework more than the underlying technology.
I thought CAF sucked and I found out the modules for it sucked.
Then I thought the provider sucked and I found out the framework for it sucks.

At first I compared TF with git.
The state file is really your repo and the infrastructure is your deployment (running code).
Unlike git you cannot pull changes, you must have the source code of your colleague for the infrastructure,
otherwise you'd destroy resources. Unfortunately Terraform doesn't let you "pull" backfill changes so easily.
If you constrain yourself to whatever's in the code should be in the cloud it kinda works great, except:
1. there are more things in the cloud than in your code that are not yet imported or even supported by TF
2. meta dependencies (such that are hard to express between resources) exist
   - you can't change a key inside a keyvault if you don't have networking access
   - you have to have a more _imperative_ approach - do 2-3 commits (which is hard when you need to get approvals)

The cool part is you get a really nice interface for multicloud integration.
Essentially the provisioning node/cluster/machine becomes a central place of configuration
and each cloud connects to it.

What you should manage with terraform?
Anything that is CRUD-like and has a low velocity of changes.
Anything relating to user access management.

There are 2 main ways to utilize terraform:
You either manage everything (95%+) through it, or you have a decent scheduled import script.

## Methology 1

This is great for environments where changes are supposed to be infrequent and access is supposed to be restricted,
like any prod environmnet. It is also great because it ensure almost 100% identical test setup.
However access must be strictly restricted. Otherwise configuration drift gets out of hand.


## Methology 2

This is mostly for visibility. It is much easier to manage 3 files of 1KLoC permissions (that can then be further template-ized to a few hundred LoC with modules) than it is to manage 3 different services with different permission models, groups, etc.
It shifts the idea that a single should administer access to systems. Instead an admin sets up an environment
where any person may submit an access request and it is only a matter of PR approval to get it configured.

In this case many more resources may exist, other management groups, users, roles etc.
Identity-and-Access-Management-as-Code (IAM-as-Code) is cool for visibility. Systems are still designed
to give out-of-code access to include / manage new users and roles.
The most useful solution here is to have a strong import / codegen process.
This makes it a 2 step circle:

import resources (users, groups, roles) -> manage idenity and access (refactor code) -|
        ^                                                                             |
        |                                                                             |
        |-----------------------------------------------------------------------------|

Prefer doing it through code for non-urgent matters but keep the opportunity to quickly administer.
One downside is everyone can see everyone else's access but I guess that's solvable in your source control tool.

## Thesis

My thesis is that software needs to simple.
Terraform (and stateful infrastructure as code frameworks)
