+++
title = "Docker"
date = 2025-11-17
+++

## Colima Runtime on MacOS

I use [colima](https://github.com/abiosoft/colima) as container runtime on MacOS.  
So if you get an error like this:
```
Cannot connect to the Docker daemon at unix:///Users/mitiko/.colima/default/docker.sock.
Is the docker daemon running?
```
You should start the runtime first:

```bash
colima start
```

More troubleshooting:
- <https://github.com/abiosoft/colima/issues/243>
- `echo 'export DOCKER_HOST="unix://$HOME/.colima/docker.sock"' >> ~/.zshrc`