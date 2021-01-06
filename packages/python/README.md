# rez-python

Currently available versions :

* 2.7.18
* 3.7.9

build command example:

```
rez-build --install --version 3.7.9
```

### Notes

Previously, I use miniconda to deploy Python, but without calling `conda activate`, it will never be safe and may not work in future conda release (conda may strictly requires a real activation in future).

However, building from Python source for each version was not easy on Windows.

So I tried downloading binary installer `.msi`/`.exe` from `python.org` and install it into Rez package. But it refused to install because it detect pre-installed Python on my system. Which is not an ideal way for achieving a reproducible Rez deployment.

In the end, I decide to manually upload the payload that extracted from the binary installer into GitHub release attachment, and simply download and extract them to deploy.
