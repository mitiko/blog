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

## Crack passphrase

I forgot the passphrase to my key - must've been a good vacation, plus muscle memory is not to be relied upon.
So here's a simple Python script to recover it based on keywords.

Obviously, it's not the most efficient way but it got the job done.  
I only remembered it starts with either phrase A or phrase B and that it ends with 2 digits.
You could, of course, plug something like [john the ripper](https://github.com/openwall/john) for a more comprehensive search space.

```py
#!/usr/bin/env python3
import subprocess

email = "your_name@gmail.com"

cmd = f'gpg --list-keys ' + email + ' | grep -oP "[A-Z0-9]{40}"'
key_id = (subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)).communicate()[0].strip().decode()
print(f"Your key = '{key_id}'")

for base in ["did_it_start_like_this", "or_like_that"]:
    for digit_1 in range(10):
        for digit_2 in range(10):
            code = f"{base}{digit_1}{digit_2}"
            # print(f"Trying {code}")
            cmd = f'echo "{code}" | gpg --batch --pinentry-mode loopback --passphrase-fd 0 --dry-run --passwd {key_id}'
            output = (subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)).communicate()[0]

            if output.find(b"Bad passphrase") == -1:
                print(f"Found code: {code}")
                exit(0)
```

**References:**
- <https://unix.stackexchange.com/questions/683084/how-can-i-check-passphrase-of-gpg-from-a-file#answer-683483>
- <https://stackoverflow.com/questions/13332268/how-to-use-subprocess-command-with-pipes#answer-13333130>
