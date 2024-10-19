+++
title = "GPG"
date = 2024-04-11
+++

## Moving keys between machines

```bash
# list keys
gpg --list-secret-keys --keyid-format LONG

# export public and secret keys
gpg --export -a $KEY_ID > gpg-pub.asc
gpg --export-secret-keys -a $KEY_ID > gpg-sc.asc

# then on host B:
gpg --import gpg-pub.asc
gpg --import gpg-sc.asc
```
