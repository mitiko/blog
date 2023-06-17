+++
title = "Terraform sucks"
date = 2023-06-17
+++

## Keypoints:
- not like git (no pull) (both good and bad)
- clouds weren't made for text (and support will recommend you not use terraform)
- pretends to be json. sucks at compile time resolution
- slow as fuck
- too many meta files (not just .git/ + .gitignore)
- error messages suck
  - can't recognize terraform errors from azure errors
  - can't copy errors easily
  - too verbose
  - cycles are hell
  - no error codes
  - can't google errors (wouldn't need to if they were good)
- too many things to name
- variables suck
- module / functions system sucks (why description on variables)
- variable validation sucks
- locals suck
- EOF strings suck
- logging sucks
- practically can't write tests (cloud testing environments / virtual resources)

## The good

Recipe for success:
- single point of deployments / applies
- documentation
- ad hoc modules with

Keep tfstate files small

## Articles / Blogs:

https://blog.gruntwork.io/terraform-up-running-3rd-edition-is-now-published-4b99804d922a
https://blog.cloudflare.com/terraforming-cloudflare-at-cloudflare/
https://blog.cloudflare.com/terraforming-cloudflare/

-- check out:
https://blog.knoldus.com/terraform-loop-with-count-and-problems/
https://blog.knoldus.com/how-to-use-terraform-graph-to-visualize-your-execution-plan/
https://www.scalr.com/blog
https://acloudguru.com/blog/tag/terraform
https://acloudguru.com/blog/engineering/5-things-we-love-about-terraform
https://www.env0.com/resources/blog
https://www.pulumi.com/blog/converting-full-terraform-programs-to-pulumi/
https://www.pulumi.com/
https://www.antonbabenko.com/
https://devdosvid.blog/2023/04/16/hello-terraform-data-goodbye-null-resource/
https://sysdig.com/blog/cloud-breach-terraform-data-theft/
https://terrateam.io/blog/the-future-of-terraform-is-clickops
https://github.com/shuaibiyy/awesome-terraform
https://blog.gitguardian.com/9-extraordinary-terraform-best-practices/
https://www.fugue.co/blog/tag/terraform
https://blog.alekc.org/categories/terraform/
