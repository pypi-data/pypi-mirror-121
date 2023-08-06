# Lancstro: an example of creating a Python package

This repository and the following text is intended as a basic tutorial on creating and publishing a
Python package. It was created for a seminar given to the Lancaster University [Observational
Astrophysics
group](https://www.lancaster.ac.uk/physics/research/astrophysics/observational-astrophysics/), but
may be more widely applicable.

## What is a Python package

In general, when talking about a [Python
package](https://docs.python.org/3/tutorial/modules.html#packages) it means an set of Python modules
and/or scripts and/or data, that are installable under a common namespace (the package's name). A
package might also be referred to as a library. This is different from a collection of individual
Python files that you have in a folder, which will not be under a common namespace and are only
accessible if their path is in your `PYTHONPATH` or you use them from the directory in which they
live.

A couple of examples of common Python packages used in research in the physical sciences are:

1. [NumPy](https://numpy.org/)
2. [SciPy](https://www.scipy.org/scipylib/index.html)

> Note: "namespace" basically refers to the name of the package as you would import it, e.g., if you
> import numpy with `import numpy`, then you will access all NumPy's functions/classes/modules via
> the `numpy` namespace:
> ```python
> numpy.sin(2.3)
> ```

A package can contain everything within a single namespace, or contain various submodules, e.g.,
parts that contain common functionality that naturally fits together in it's own namespace. For
example, in NumPy, the [`random`](https://numpy.org/doc/stable/reference/random/index.html)
submodule contains functions and classes for generating random numbers:

```python
import numpy
numpy.random.randn()  # generate a normally distributed random number
```

## Why package my code?

So, why should you package (and publish) your Python code rather than just having local scripts?
Well, there are several reasons:

* It creates an installable package that can be imported without having to have the Python
  script/file in your path.
* It creates a “versioned” package that can have specified features/dependencies. This is very
  important for reproducibility of results, where a specific code version used for an analysis
  can be pointed to.
* You can share you package with others (you can make it `pip installable` via
  [PyPI](https://pypi.org/), or `conda installable` via [conda-forge](https://conda-forge.org/)),
  which can be important when working with collaborators.
* You will gain developer kudos! Software development is a major skill you learn during your
  research, so show off what you’ve done and add it to your CV.

## Project structure

To create a Python package you should structure the directory containing you code in the following
way (the directory name containing this information does not have to match the package name, but
often they will):

```
repo/
├── LICENSE
├── pyproject.toml
├── README.md
├── setup.cfg
├── setup.py
├── pkgname/
│   ├── __init__.py
│   └── example.py
└── bin/
    └── executable_script.py
```

There are other slight variations on this, for example, using a `src` directory in which your
package directories live, as described in the [official
guidelines](https://packaging.python.org/tutorials/packaging-projects/#creating-the-package-files)).

In this project the structure is:

```
lancstro/
├── LICENSE
├── pyproject.toml
├── README.md
├── setup.cfg
├── setup.py
├── lancstro/
│   ├── __init__.py
│   ├── base.py
|   ├── members/
|   |   ├── __init__.py
|   |   └── staff.py
|   └── data/
|       └── office_numbers.txt
└── bin/
    └── favourite_object.py
```

Here, there is a "submodule" called `members` within the main `lancstro` package.

### Using Github

Your package *should* be in a [version control](https://en.wikipedia.org/wiki/Version_control)
system and ideally hosted somewhere that provides a backup. It is now very common to use
[git](https://git-scm.com/about) for version control and it is sensible to host the project on
[Github](https://github.com/)/[Gitlab](https://about.gitlab.com/)/[bitbucket](https://bitbucket.org/product/)
or similar. On Github you can have public or private repositories.

If using Github, it is best to start the project by creating new repository there first, then
cloning that repository to you machine before then adding in your code. When creating a Github
repository (I might use "_repo_" for short later) you can initialise it with a [license
file](#the-license-file) and a [README file](#the-readmemd-file).

> Note: this is not a tutorial on using git, so you'll have to find that
> [elsewhere](https://git-scm.com/docs/gittutorial).

### The LICENSE file

You should give your code a license describing the terms of use and copyright. Often you'll want
your code to be open source, so a good choice is the [MIT
license](https://opensource.org/licenses/MIT), which is very permissive in terms of reuse of the
code. A [variety of other open source licenses](https://opensource.org/licenses/category) are
available, although these often differ slighty on the permissiveness, i.e., whether others can use
your code in commercial and non-open source projects or not.

The `LICENSE` file will contain a plain ascii text copy of your license.

### The pyproject.toml file

This file tells the [`pip`](https://packaging.python.org/key_projects/#pip) tool used for installing
packages how it should build the package. In this repo we have used the [file
contents](pyproject.toml) suggested
[here](https://packaging.python.org/tutorials/packaging-projects/#creating-pyproject-toml), which
means that the [`setuptools`](https://setuptools.pypa.io/en/latest/index.html) package is used for
the build.

### The README.md file

This is the file that you are currently reading! It should provide a basic description of your
package, maybe including information about how to install it. Ideally it should be brief and not be
seen as a replacement for having proper [documentation](#documentation) for you code available
elsewhere.

In this case the suggested format for the file is
[Markdown](https://daringfireball.net/projects/markdown/) (the `.md` extension), but it could be a
plain ascii text file or [reStructedText](https://docutils.sourceforge.io/rst.html). Markdown and
reStructuredText will be automatically rendered if you host your package on, e.g.,
[Github](https://github.com/).

### The setup.cfg and setup.py files

In many packages you might just see a `setup.py` file, which is the build script used by setuptools.
However, it is now good practice to put ["static"
metadata](https://packaging.python.org/tutorials/packaging-projects/#configuring-metadata) about
your package in the `setup.cfg` [configuration
file](https://en.wikipedia.org/wiki/Configuration_file#Unix_and_Unix-like_operating_systems). By
"static" I mean any package information that does not have to be dynamically defined during the
build process (such as defining and building Cython
[extensions](https://setuptools.pypa.io/en/latest/userguide/extension.html)). In many cases, like
this repository, this can mean the [`setup.py`](setup.py) file can be very simple and just contain:

```python
from setuptools import setup

setup()
```

The layout of the configuration file is described
[here](https://setuptools.pypa.io/en/latest/userguide/declarative_config.html). I'll reproduce the
[one from this project](setup.cfg) below with additional inline comments:

```toml
[metadata]
# the name of the package
name = lancstro

# the package author information (multiple authors can just be separated by commas)
author = Matthew Pitkin
author_email = m.pitkin@lancaster.ac.uk

# a brief description of the package
description = Package defining the Lancaster Observational Astronomy group

# the license type and license file
license = MIT
license_files = LICENSE

# a more in-depth description of the project that will appear on it's PyPI page,
# in this case read in from the README.md file
long_description = file: README.md
long_description_content_type = text/markdown

# the projects URL (often the Github repo URL)
url = https://github.com/mattpitkin/lancstro

# standard classifiers giving some information about the project
classifiers =
    Intended Audience :: Science/Research
    License :: OSI Approved :: MIT License
    Natural Language :: English
    Programming Language :: Python
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.6
    Programming Language :: Python :: 3.7
    Programming Language :: Python :: 3.8
    Programming Language :: Python :: 3.9
    Topic :: Scientific/Engineering
    Topic :: Scientific/Engineering :: Astronomy
    Topic :: Scientific/Engineering :: Physics

# the package's current version (this isn't actually in the file in this repo, see later!)
version = 0.0.1

[options]
# state the Python versions that the package requires/supports
python_requires = >=3.6

# state packages and versions (of necessary) required for running the setup
setup_requires =
    setuptools >= 43
    wheel

# state packages and versions (if necessary) required for installing and using the package
install_requires =
    astropy
    astroquery >= 0.4.3

# automatically find all modules within this package
packages = find:

# include data in the package defined below
include_package_data = True

# any executable scripts to include in the package
scripts =
    bin/favourite_object.py

[options.package_data]
# any data files to include in the package (lancsrto shows they are in the
# lancstro package and then the paths are given)
lancstro = 
    data/office_numbers.txt
```

For a list of the standard "classifiers" that you can add see [here](https://pypi.org/classifiers/).

In this project, we have added a "data" file that come bundled with the package. It is not required
to include data in your package.

#### Adding a package version

In the above case the package version is set manually in the `setup.cfg` file. It is up to you how
you define the version string, but it is often good to use [Semantic
Versioning](https://semver.org/). In this format the version consists of three full-stop separated
numbers: MAJOR.MINOR.PATCH.

The Semantic Versioning site gives the following definitions of when to change the numbers:

> 1. MAJOR version when you make incompatible API changes,
> 2. MINOR version when you add functionality in a backwards compatible manner, and
> 3. PATCH version when you make backwards compatible bug fixes.
>
> Additional labels for pre-release and build metadata are available as extensions to the
> MAJOR.MINOR.PATCH format.

To update the version you can just edit the value in the `setup.cfg` file. When you
[install](#installing-the-package) this will be the package's version.

This allows the package manager (e.g., pip) to know what version of the package is installed.
However, it is often useful to provide the version number as a variable within the package itself,
so that the user can check it if necessary. Most often you will find this as a variable called
`__version__`, e.g.,:

```python
import numpy
print(numpy.__version__)
1.21.2
```

There are several ways to set this, but it is best to make sure that there's only one place that you
have to edit the version number rather than multiple places. One method (used in this package) is to
include the version number in your package's main [`__init__.py`](cwinpy/__init__.py) file by adding
the line:

```python
__version__ = "0.0.1"
```

Then, within `setup.cfg`, the `version` line can be:

```
version = attr: lancstro.__version__
```

Among the other options, a good one to use is through setting the version with a tools such as
[`setuptools-scm`](https://pypi.org/project/setuptools-scm/), which gathers the version information
from [git tags](https://git-scm.com/book/en/v2/Git-Basics-Tagging) in your repo.

#### The MANIFEST.in file

You can specify which additional files that you want to be bundled with the package's source
distribution using a [`MANIFEST.in`](https://packaging.python.org/guides/using-manifest-in/). With
modern versions of setuptools (e.g., greater than 43) most of the standard files such as the README
file and setup files, and any license file given in `setup.cfg`, are automatically included in the
source distribution by default. Hence, not include a `MANIFEST.in` file in this repository.

However, you may want to include other files. If you had, say, a `test` directory with multiple
Python test scripts that you wanted in the package, you could add and `MANIFEST.in` file containing:

```
recursive-include test/ *.py
```

which will include all `.py` files within `test`.

### The package source directory

In this project the directory containing the package source code, i.e., the Python files, is called
`lancstro/`. In this case has two files in it (although it can contain any number of Python files, each of
which will be a module that is available in the package):

1. [`__init__.py`](lancstro/__init__.py)
2. [`base.py`](lancstro/base.py)

The [`base.py`](lancstro/base.py) file contains some Python code, in this case a class called
`GroupMembers`, which is part of our package.

The [`__init__.py`](lancstro/__init__.py) file is very important. It is what tells Python that this
directory is a [package](https://docs.python.org/3/tutorial/modules.html#packages). The
`__init__.py` file can be completely empty, but it *does* need to be present. It can contain any
Python code (you could define your whole package in the `__init__.py` file if you wanted), but often
it is used to import things from submodules/subpackages into the package's namespace. In this case
the `__init__.py` file contains the following code:

```python
from .base import GroupMember
from . import members

__version__ = "0.0.2"  # the version number of the code
```

The first line imports the `GroupMember` class from the [`base.py`](lancstro/base.py) file, so that
the `GroupMember` class can be used from the `lancstro` namespace rather than the `lancstro.base`
namespace. E.g., this means that when using the package we could do:

```
from lancstro import GroupMember
```

rather than

```
from lancstro.base import GroupMember
```

although both will work. You may want to do this for commonly used function or classes, but it is
not necessary.

The `lancstro/` directory also contains the directory `members/`, which is a subpackage of the
package (any subpackage must also contain their own [`__init__.py`](lancstro/members/__init__.py)
file). The second line of the `__init__.py` file imports the `members` submodule into the `lancstro`
namespace. E.g., if I just do:

```python
import lancstro
```

then I can access things from the `members` subpackage using

```python
lancstro.members.staff
```

rather than doing:

```
from lancstro.members import staff
```

although (again) both will work.

The final line in the `__init__.py` file sets the [version number](#adding-a-package-version) of the
package.

#### The data directory

You might want to include some data files in your package, e.g., a look-up table for a calculation,
a catalogue, etc. In this case I've added a JSON file,
[`office_numbers.txt`](lancstro/data/office_numbers.txt), in a directory called `data/` (any name
can be used, but `data` seems quite sensible!). This directory does not need an `__init__.py` as it
is not a package. To include this file in the package you need to have the line:

```
include_package_data = True
```

in your `setup.cfg` file and also list it in the `[options.package_data]` section, e.g.,:

```
[options.package_data]
lancstro = 
    data/office_numbers.txt
```

#### Intra-package references

In your package you can
[import](https://docs.python.org/3/tutorial/modules.html#intra-package-references) things from the
various submodules/subpackages using the `.` notation.

For example, to import things between Python files in the same part of the package (e.g., at the
`lancstro/` level), you can do:

```python
from .base import GroupMember
```

which imports from the `base.py` file.

If a file in a subpackage wants to import from the level below, e.g., a Python file in
`lancstro/members` wants to import from a file in `lancstro/`, the you could use:

```python
from ..base import GroupMember
```

I.e, use two dots `..` to specify going down one package level.

### The bin directory

You may want to include executable scripts in your package. It is good to place them in a directory
called, for example, `bin/` in the root directory of your repository. To make these part of the
package you need to list these in the `setup.cfg` file in a `scripts` section, e.g.,

```
scripts =
    bin/favourite_object.py
```

Once the packages are installed these scripts should be in you path and usable with, e.g.,:

```bash
$ favourite_object.py -h
```

### Installing the package

It is best practice to install Python packages using [pip](https://pip.pypa.io/en/stable/) (the
"package installer for Python"), so you should have that installed. Once you have the above
structure you can install the package (from it's root directory) using:

```bash
pip install .
```

where the `.` just refers to the current directory. The standard install locations are described
[here](https://docs.python.org/3/install/index.html#how-installation-works), but I would recommend
using [virtual environments](https://realpython.com/python-virtual-environments-a-primer/), such as
provided via [conda](https://docs.conda.io/en/latest/), in which case the package will be installed
only in the environment.

That's it! Open up a Python terminal (from any location except in the package directory, otherwise
it'll get confused!) and you should be able to do:

```python
import lancstro
print(lancstro.__version__)
0.0.1
```

or run the [`favourite_object.py`](bin/favourite_object.py) script from the command line:

```console
$ favourite_object.py -h
usage: favourite_object.py [-h] name name

Get a staff member's favourite object

positional arguments:
  name        The staff member's full name

optional arguments:
  -h, --help  show this help message and exit
```

You can then tell other people to clone your Github repo and install things in the same way, or even
`pip install` directly from the repo with, e.g.:

```bash
$ pip install git+git://github.com/mattpitkin/lancstro.git#egg=lancstro
```

These methods will install the very latest code from the repo, so not necessarily a specific version
(although that can be done if you've tagged a version or work from a particular the git hash).

### Publishing the package on PyPI

Rather than getting people to install code directly from your Github repo, it is often better to
publish versioned releases of your code. You can publish Python packages on the
[PyPI](https://pypi.org/) (Python Package Index) repository from which they will then be `pip
installable` by anyone!

Firstly, you'll need to [register an account](https://pypi.org/account/register/) on PyPI. Anyone is
able to do this. Secondly, you'll need to install the
[`twine`](https://twine.readthedocs.io/en/latest/) package, which is used for uploading packages to
PyPI.

Within your repo's root directory (containing `setup.py`) you can now build a [Python
wheel](https://pythonwheels.com/) (a zipped binary format of the package designed for speedier
installation) containing your package with:

```bash
python setup.py bdist_wheel sdist
```

> Note: if your code is pure Python, creating a wheel should work straightforwardly, but if not the
> wheel generation may not work. In these cases you can just build a tarball containing the package
> using:
>
> ```bash
> python setup.py sdist
> ```

This should create a `dist/` directory containing a file with the extension `.whl` (built by
including the `bdist_wheel` argument). This is the Python wheel. It should also contain a tarball of
the package (built by including the `sdist` argument).

It is often best to first upload these products to [PyPI's testing
repository](https://packaging.python.org/guides/using-testpypi/) (you'll need to [register a
separate account](https://test.pypi.org/account/register/) for this), which can be done using
`twine` with:

```bash
twine upload -r testpypi dist/*
```

> Note: make sure the `dist/` directory is empty before generating the new package version with
> `python setup.py bdist_wheel sdist` otherwise you might end up uploading multiple versions.

You should be prompted for your username and password, although there are ways to set these as
[environment variables](https://twine.readthedocs.io/en/latest/#environment-variables) or
[using](https://twine.readthedocs.io/en/latest/#keyring-support)
[`keyring`](https://pypi.org/project/keyring/), so that you don't have to enter them each time. If
the upload is successful you should be able to see the project on the Test PyPI site, e.g., at
https://test.pypi.org/project/lancstro/0.0.2/.

You can test that the package installs correctly from the Test PyPI repository by running
(potentially in a new virtual environment):

```bash
pip install -i https://test.pypi.org/simple/ lancstro
```

If you're happy with the package you can proceed to upload it to the main PyPI repository using:

```bash
twine upload dist/*
```

Et voilà! Now you just need to tell people to run:

```bash
pip install lancstro
```

to install your [package](https://pypi.org/project/lancstro/0.0.2/). If they want to install a
particular version they can use, e.g.,:

```bash
pip install lancstro==0.0.2
```

Or, if there's a lower or upper version that must be used the inequality operators can be used
instead, e.g.,:

```bash
pip install lancstro<=0.0.2
```

### Publishing the package on conda-forge

You may (and _should_!) install Python packages in a virtual environment that is relevant for the
particular project that you are working on. A popular virtual environment/package manager tool is
[conda](https://docs.conda.io/en/latest/), which is installed as part of
[Anaconda](https://www.anaconda.com/). Conda is a package manager for a variety of software, not
just Python packages, so if creating a conda package for your Python project you can make it
dependent on specific versions of non-Python libraries (maybe you want to use a specific version of
[GSL](https://www.gnu.org/software/gsl/)!).

You can [build a conda
package](https://docs.conda.io/projects/conda-build/en/latest/user-guide/tutorials/build-pkgs.html)
and host it in your own account on Anaconda.org. However, a popular repository for hosting projects
is [conda-forge](https://conda-forge.org/). An advantage of hosting your package on conda-forge is
that it will have been automatically verified by a test suite and reviewed by an actual person, so
hopefully will be more robust for other users.

Getting a package on conda-forge is quite a bit more involved than uploading to PyPI, although if
you already have your package on PyPI that is an advantage (and is what I'll assume in the example
below). The basic steps are given [here](https://conda-forge.org/#add_recipe), but you will need a
Github account. I'll detail these a bit more below.

> Note: you will need to have uploaded the package source tarball to PyPI for these instructions to
> work.

1. Go to https://github.com/conda-forge/staged-recipes and fork the repository to your own account.
2. In your fork of the repository create a new branch. If you've cloned your fork of the repository
   you might do:

   ```bash
   git checkout -b add_lancstro_to_conda_forge
   ```
3. In the `recipes/` directory create a new directory with the name of your package and copy the
   [`meta.yaml`](https://github.com/conda-forge/staged-recipes/blob/main/recipes/example/meta.yaml)
   file from the `example/` directory into it:

   ```bash
   cd recipes
   mkdir lancstro
   cp example/meta.yaml lancstro
   ```
4. Open up the copied `meta.yaml` file in a text editor and change it to look something like below
   (I've removed a lot of the comments):

```yaml
{% set name = "lancstro" %}
{% set version = "0.0.1" %}

package:
  name: {{ name|lower }}
  version: {{ version }}

source:
  url: https://pypi.io/packages/source/{{ name[0] }}/{{ name }}/{{ name }}-{{ version }}.tar.gz
  # get the SHA256 check sum of the file (on the PyPI page for the package
  # click on "Download files" and then "View" under the "Hashes" heading)
  sha256: 2873bb17f5e8cc84ac19e22307cc8567273fcdc57e5dd1f57fe52b2b1a6b1da3

build:
  noarch: python
  number: 0
  script: "{{ PYTHON }} -m pip install . -vv"

requirements:
  host:
    # packages required to build and install the package
    - python
    - pip
    - setuptools
  run:
    # packges required to run the package
    - astropy
    - astroquery >= 0.4.3
    - python

test:
  # make sure the package can at least be imported (other tests can be added)
  imports:
    - lancstro

about:
  home: https://github.com/mattpitkin/lancstro
  license: MIT
  license_family: MIT
  summary: 'My great package'
  description: |
    An example package for showing how to package a package.
  doc_url: https://lancstro.readthedocs.io/
  dev_url: https://github.com/mattpitkin/lancstro

extra:
  recipe-maintainers:
    # github ids for maintainers
    - mattpitkin
```
5. Commit the changes and push them to your fork of the `staged-recipes` repository.
6. Open up a pull request (PR) between your branch and conda-forge's `staged-recipes` repo. Call the
   PR something like "Add lancstro". Create the pull request.
7. After a while check that the test builds in the PR have completed successfully. If not try and
   fix the issue by editing the (forked) `meta.yaml` file.
8. Answer and respond to any questions/comments from the assigned reviewer (you shouldn't have to
   assigned a reviewer, but sometimes you need to prod the appropriate channel).
8. Wait for a reviewer to sign-off and merge the PR.

At this point your package should be installable from conda-forge using, e.g.,:

```bash
conda install -c conda-forge lancstro
```

## Documentation

You should try not to just write code for yourself. Academic results should be transparent and
reproducible, so the code you write and use should be usable by others, therefore _Write The Docs_!

Creating documentation for your code doesn't just mean that your code should contain comments (which
it definitely should!), but there should also be documentation (on, e.g., a website) on how to
install and use your code. This should include information on the code's
[API](https://en.wikipedia.org/wiki/API) (just a fancy way of saying show how to use the functions
and classes in your package). It is also important to have examples of use cases as it's often good
to "_show not tell_". You can store the documentation source files in the same repository as you
package (e.g., a `docs/` folder).

I'm not going to describe in detail how to add documentation to a package (I haven't added it into
this package yet, but I may add this in the future!), but will just point towards some resources.
Two packages that you may want to look into for building documentation are:

1. [Sphinx](https://www.sphinx-doc.org/en/master/)
2. [mkdocs](https://www.mkdocs.org/)

Both of these allow you to write documentation in Markdown or reStructuredText and automatically
include (via various extensions/plugins) code docstrings. They can also include Jupyter notebooks.

For repositories hosted on Github, you can easily and freely set up building and hosting of the
documentation on [Read the Docs](https://readthedocs.org/). You can also publish your [documentation
directly](https://github.blog/2016-08-22-publish-your-project-documentation-with-github-pages/) on
Github using [Github Pages](https://pages.github.com/).

There is an example of using Sphinx for documenting a package
[here](https://matplotlib.org/sampledoc/).

### Contributions

Your code may be the product of many developer's work. If it's open source you may also be open to
having other developers contributing to it. You should therefore have instructions on how people
should contribute and guidelines on the expected behaviour of contributors.

Often you will see a `CONTRIBUTING.md` Markdown file in package repositories that describes how to
contribute. If a contributor wants to add/request a new feature, or fix a bug, then they may want to
open a Github issue (or post on an appropriate forum) to see if the feature is useful/bug is known.
If they have coded up a bug fix/feature then adding that into the repository often involves a
"[fork-and-pull request](https://gist.github.com/Chaser324/ce0505fbed06b947d962)" workflow process
(this is the process for many projects, e.g.,
[NumPy](https://numpy.org/doc/stable/dev/development_workflow.html),
[astropy](https://docs.astropy.org/en/latest/development/workflow/development_workflow.html)):

1. fork the repository to your own Github account
2. create a new branch on your fork for development
3. add and commit your changes making sure that they work and don't break the package
4. push your commits to your fork
5. create a pull request with the upstream (i.e., original) repository
6. respond to any comments on the change
7. merge the request into the original repository

#### Code of conduct

You should also consider adding a code of conduct to your project outlining expected behaviours
during interactions between developers/contributors. There are many examples of code's of conduct
that you can often use verbatim (many are licensed using [Creative
Commons](https://creativecommons.org/licenses/by/4.0/) licenses) or adapt to your needs:

* [astropy code of conduct](https://www.astropy.org/code_of_conduct.html)
* [NumFOCUS code of conduct](https://numfocus.org/code-of-conduct)
* [Python Community code of conduct](https://www.python.org/psf/conduct/)

#### Code style

You may want to enforce a particular style for your code. Many projects follow the
[PEP8](https://www.python.org/dev/peps/pep-0008/) style guide. There are packages that you can run
on your code to automatically make them conform to this style, e.g.,
[black](https://black.readthedocs.io/en/stable/) or [flake8](https://flake8.pycqa.org/en/latest/),
so you should tell contributors to run these on any code they submit (and make sure you run them
yourself!). You can also add the [pep8speaks](https://pep8speaks.com/) app on Github that will check
that any pull request conforms to PEP8 and inform the committer of any violations of the style.

You can force checks to happen automatically by using the [pre-commit](https://pre-commit.com/)
package to add ["pre-commit" hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks) to
git, so that it automatically runs, e.g., black, on any committed code.

## Making code citable

Your code is a very large part of your academic output, so it's good to make your package citable.
This way you can receive appropriate acknowledgement when people use it and show evidence of your
output. There are a variety of ways of doing this (skewed towards Astro/Physics):

* For packages on Github, link your repository to [Zenodo](https://zenodo.org/) which will provide
  a citable [DOI](https://www.doi.org/) for you project.
* Get it linked onto the [Astrophysics Source Code Library](https://ascl.net/) (ASCL). This is
  indexed on NASA ADS, but does not give a DOI.
* Write a paper for the [Journal of Open Source Software](https://joss.theoj.org/) (JOSS). This is a
  very light touch, but peer reviewed publication that also provides a DOI and is indexed on NASA
  ADS. It does require you to have proper documentation for your package as an acceptable level of
  documentation is part of the review.
* Write a paper for a standard journal. Many journals (_MNRAS_, _ApJ_, _PASP_, etc) do now accept
  papers on software, although it's likely that they should also include a description of a
  practical use case for the software.

## Not covered here!

There are many additional useful things that I've not covered here. These include:

* using entry point console scripts rather than, or as well as, including executable scripts
* including C/C++/FORTRAN code, or [Cython](https://cython.org/)-ized code, in your package
* creating a [test suite](https://docs.pytest.org/) for your package (and checking its
  [coverage](https://pytest-cov.readthedocs.io/en/latest/))
* setting up [continuous integration](https://en.wikipedia.org/wiki/Continuous_integration) for
  building and testing (and automatically publishing) your code (e.g., with [Github
  Actions](https://docs.github.com/en/actions), TravisCI, ...)

I may add these at a later date.

## Other resources

For other descriptions of creating your Python code see:

* [Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/)
* [`setuptools` documentation](https://setuptools.pypa.io/en/latest/index.html)
* ["How to package your Python code"](https://python-packaging.readthedocs.io/en/latest/index.html)
