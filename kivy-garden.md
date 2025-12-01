  Kivy Garden by kivy-garden    

[![Kivy](stylesheets/logo-kivy.png)](http://kivy.org/)

*   [Guides](http://kivy.org/docs/gettingstarted/intro.html)
*   [Garden](http://kivy-garden.github.io)
*   [API Reference](http://kivy.org/docs/api-kivy.html)
*   [PDF](http://kivy.org/docs/pdf/Kivy-latest.pdf)
*   [Wiki](http://wiki.kivy.org)

### Kivy Garden

*   [General Usage Guidelines](index.html#generalusageguidelines)
*   [Development Guidelines](index.html#developmentguidelines)
*   [Making a release for your flower](index.html#makingareleaseforyourflower)
*   [Disabling notification spam](index.html#disablingnotificationspam)
*   [Transferring repository](index.html#transferringrepository)
*   [Legacy Garden Tool General Usage Guidelines](index.html#legacygardentoolgeneralusageguidelines)
*   [Guide for migrating flowers from legacy structure](index.html#guideformigratingflowersfromlegacystructure)
*   [Gallery](gallery.html)

Welcome to Kivy Garden
======================

This is an organization for developers of Kivy widgets, add-ons and related software.

If you have a kivy flower you'd like to contribute to garden see [Developing a new flower](#developinganewflower).

Memberships are granted for users who have contributed to existing garden flowers in the past year or have submitted their own flower in the application. Please note that memberships expire after a year of inactivity.

The garden flower widgets are contributed by regular users such as yourself. The kivy developers do not take any responsibility for the code hosted in the garden organization repositories - we do not actively monitor the flower repos. Please use at your own risk.

Update to garden structure
--------------------------

Starting with the kivy 1.11.0 release, kivy has [shifted](https://github.com/kivy/kivy/wiki/Moving-kivy.garden.xxx-to-kivy_garden.xxx-and-kivy.deps.xxx-to-kivy_deps.xxx) from using the garden legacy tool that installs flowers with `garden install flower` and where the flower does not have a proper python package structure to flowers that can be installed with pip and uploaded to pypi. Kivy supports the legacy garden flowers side by side with the newer packages so the garden tool and legacy flowers will be able to be used indefinitely. But we will only provide support for the newer packages format in the future.

For garden package maintainers - for a guide how to migrate your garden package from the legacy structure `garden.flower` to the newer `flower` structure used with the pip, see [this guide](#guideformigratingflowersfromlegacystructure).

General Usage Guidelines
------------------------

To use a kivy garden flower, first check if the flower is in the legacy format. If the flower name is in the format of `garden.flower`, such as [garden.graph](https://github.com/kivy-garden/garden.graph) it is a legacy flower. If it is just `flower` such as [graph](https://github.com/kivy-garden/graph) it is in the present format. If it is in the legacy format see [Legacy Garden Tool General Usage Guidelines](#legacygardentoolgeneralusageguidelines) for how to install and use it. Otherwise, continue with the guide below.

Garden flowers can be installed with the `pip` tool like a normal python package. Given a flower that you want to install, lets use [graph](https://github.com/kivy-garden/graph) as an example. You can install it directly from github master with:

    python -m pip install https://github.com/kivy-garden/graph/archive/master.zip
                

Look under the repository's releases tab if you'd like to install a specific release or a pre-compiled wheel, if the flower has any. Then use the url with `pip`.

Or you can automatically install it using garden's pypi server with:

    python -m pip install kivy_garden.graph --extra-index-url https://kivy-garden.github.io/simple/
                

To permanently add our garden server to your pip configuration so that you don't have to specify it with `--extra-index-url`, add

    [global]
                timeout = 60
                index-url = https://kivy-garden.github.io/simple/
                

to your [pip.conf](https://pip.pypa.io/en/stable/user_guide/#config-file).

If the flower maintainer has uploaded the flower to [pypi](https://pypi.org/), you can just install it with `pip install kivy_garden.flower`.

Development Guidelines
======================

Developing a new flower
-----------------------

If your flower will be a pure python flower start with the pure python [demo](https://github.com/kivy-garden/flower). If it is a cython flower, start with this [demo](https://github.com/kivy-garden/cython_flower).

1.  Create a new empty repository in your github account named `widgetname` (the lowercase name of the widget you're contributing).
    
2.  Clone the demo repo locally (the following instructions use git ssh urls, replace `git@github.com:your_github_username` with `https://github.com/your_github_username` if you don't have `ssh` set up):
    
        git clone git@github.com:kivy-garden/flower.git widgetname
                    
    
    or if will be a cython flower:
    
        git clone git@github.com:kivy-garden/cython_flower.git widgetname
                    
    
    You'll be modifying the demo flower to contain your own widget.
    
3.  Now mirror the demo to your account and fix the git origin to point to your account: `sh cd widgetname git push --mirror git@github.com:your_github_username/widgetname.git git remote set-url origin git@github.com:your_github_username/widgetname.git`
    
4.  Start customizing the demo repo for your flower:
    
    1.  Rename the `kivy_garden/flower` directory to `kivy_garden/widgetname`.
    
    4.  Replace the contents of `kivy_garden/widgetname/__init__.py` with code for your widget. People will be importing your new widget with `from kivy_garden.widgetname import WidgetName` so make sure that works.
    
    7.  Fix the tests in `tests/` to test your widget. The test are run with pytest. Try to test as much as you can.
    
    10.  Fix the `README.md` with basic information about your widget.
    
    13.  Fix `setup.py` to replace all references of `flower` with `widgetname` and everything else as appropriate.
    
    16.  Test install it to python and use it in your app to see if it works: `sh pip install -e .` This installs it in place so you can test and change the source code directly without having to reinstall every time. To test: `sh python -c "from kivy_garden.widgetname import WidgetName"` If it's a cython flower, compile it after any changes: `sh python setup.py build_ext --inplace` To run the tests: `sh python -m pytest tests/`
    
    19.  If you enable travis integration for your new `widgetname` repo on github, the code will be automatically tested on travis after every commit (see the `.travis.yml` file - you shouldn't need to change anything there). Kivy-garden will automatically run travis integration on all flowers, so make sure it works.
    
    22.  Finally, add your changes, commit and push all your changes to github: `sh git push origin master`
    
    25.  Make sure that travis runs without failures, otherwise fix and push etc.
    

7.  Now that the `widgetname` repo is ready, you're ready to transfer it into kivy-garden. See [Transferring repository](#transferringrepository).
    

10.  To make the project installable with `pip`, you'll need to add it to garden's simple pypi server.
    
    1.  Fork the [garden website](https://github.com/kivy-garden/kivy-garden.github.io) into your account.
    
    4.  Take a look at how the current flowers are [listed](https://github.com/kivy-garden/kivy-garden.github.io/tree/master/simple) and add a similar new file for your flower (`kivy-garden-widgetname/index.html`).
    
    7.  Add your flower to the root `simple/index.html` file.
    
    10.  Make a pull request to the original [repo](https://github.com/kivy-garden/kivy-garden.github.io) and link to it in your issue that requests that your flower be added to kivy-garden that you opened in [Transferring repository](#transferringrepository).
    

13.  In the future if you want tp make a release to your flower and change the version, see [Making a release for your flower](#Making a release for your flower) for how to make a release and add these releases to the pypi server.
    

Flower guidelines
-----------------

1.  Code added to the garden **must be licensed under MIT** (same as Kivy) and a LICENSE file must be added to every repository.
    
2.  Keep the Widget and add-on simple. **Do one task and do it well**.
    
3.  Name your widget correctly. Don't put "Widget" in the widget name as this is obvious. (SliderWidget, ProgressBarWidget are wrong, keep it simple.)
    
4.  Create adequate documentation that explains the functionality of your widget. A doc directory using sphinx documentation is adequate, or just nice docs in the actualy code or readme.
    
5.  Follow the [PEP8 guidelines](http://www.python.org/dev/peps/pep-0008/) for coding standards.
    
6.  Follow the kivy [guidelines for contributing](http://kivy.org/docs/contribute.html). To install the pep8 checker into your git directory do
    
    cp path-to-kivy/kivy/tools/pep8checker/pre-commit.githook path-to-your-source/.git/hooks/pre-commit
                chmod +x path-to-garden-source/.git/hooks/pre-commit
    
    Then assuming you have kivy in your path, our style guide check will run whenever you do a commit, and if there are violations in the parts that you changed, your commit will be aborted. Fix & retry.
    
7.  Use the [`Monitor` module](http://kivy.org/docs/api-kivy.modules.monitor.html) to ensure that your widget can maintain a FPS rate above 60, ensuring smooth interaction with the user.
    
8.  Follow the [performance guidelines for Python](http://wiki.python.org/moin/PythonSpeed/PerformanceTips), like ensuring minimum lookups, avoiding lookups in loops...
    
9.  As a way of self-organizing widgets, add a screenshot named "`screenshot.png`" to the root of your repo showcasing the widget.
    
10.  Use tags instead of a directory structure to categorize your widgets in the documentation.
    

Note: you must have a GitHub account to open a ticket. You can create one for free [here](https://github.com/).

Making a release for your flower
--------------------------------

1.  Update `CHANGELOG.md` and commit the changes
2.  Update `__version__` in `kivy-garden/flower/__init__.py` (or in `kivy-garden/flower/_version.py` if it's a cython flower) to the next version and commit the change. If it's `x.y.z.dev0`, remove the `dev0` to update to the release version.
3.  Call `git tag -a x.y.z -m "Tagging version x.y.z"` to make a tag
4.  Call `python setup.py bdist_wheel --universal` (or `python setup.py bdist_wheel` if it's a cython flower) and `python setup.py sdist`, which generates the wheel and sdist in the dist/\* directory.
5.  Make sure the dist directory contains the files to be uploaded to pypi and call `twine check dist/*`
6.  Then call `twine upload dist/*` to upload to pypi.
7.  Call `git push origin master --tags` to push the latest changes and the tags to github.
8.  In github, go to the release tab and draft a new release for the tag. Upload there any wheels you generated (if any).
9.  Make a new PR that updates `https://github.com/kivy-garden/kivy-garden.github.io/blob/master/simple/kivy-garden-widgetname/index.html` to list any new wheels, sdist, and versions as needed. Link to the github release files as needed. See the [website](https://kivy-garden.github.io/simple/) for information on how to list files on a pypi server.
10.  Update `__version__` in `kivy-garden/flower/__init__.py` (or in `kivy-garden/flower/_version.py` if it's a cython flower) to the next dev (e.g. `x.y+1.z.dev0`) version and commit and push the change.

Other issues
------------

For all other issues, please open a ticket in the appropriate [repository](https://github.com/kivy-garden).

Disabling notification spam
---------------------------

By default you are subscribed to all new Garden github repository notifications. Unless you disable this yourself, your inbox will soon contain only Github spam.

Go to [https://github.com/watching](https://github.com/watching) Select what to watch or uncheck Automatically watch. But attention: latter will disable watch for all organizations.

Transferring repository
-----------------------

Once you have a flower repository ready and all the tests are passing, you're ready to transfer it to garden.

How to move your repository to Kivy Garden shared ownership?

About transferring the ownership of repositories. See Github instructions regarding transfers

Join us by opening a [new issue](https://github.com/kivy-garden/kivy-garden.github.io/issues/new?title=Please%20add%20me%20to%20Kivy%20Garden&body=Link%20for%20a%20merged%20garden%20PR%20or%20a%20proposed%20new%20flower%3A%0A%3Cgarden%20PR%20or%20transferable%20repository%20link%3E) indicating you have a flower to contribute.

Request the github name of any of the Kivy Garden administrators team on the github issue who is ready to initiate the process. Make sure they are actually an admin. Then, make them the owner of the repository which needs to be transferred. If the repository is already part of Github organization then create a new team and make the garden admin person the sole member of this team. Then assign the ownership permission of the repository to the new team. Now the garden administrator can go to the repository settings and press Transfer Ownership button

Legacy Flowers
==============

Legacy Garden Tool General Usage Guidelines
-------------------------------------------

1.  Make sure you have `requests` installed:
    
    sudo pip install requests
    
2.  Install `kivy-garden` if you don't have it:
    
    pip install kivy-garden
    
    Make sure you have the folder that contains `garden` file on your `PATH` (or `cd` to the folder).
    
    $ garden list
    
    To list all the installed garden packages
    
    $ garden search
    
    To search garden packages on GitHub
    
    $ garden install package\_name
    
    To install a garden package
    
    $ garden uninstall package\_name
    
    To uninstall a garden package
    
3.  To use a installed garden package:
    
    from kivy.garden import package\_name
    
4.  By default the installation is done in `~/.kivy/garden/garden.widgetname` so that all kivy apps can use the widget once installed.
    
    To include the package in your mobile distribution, you should install the garden package with `--app` command line argument, this way the package is downloaded and installed in your app directory and thus included in your apk.
    
    cd my\_app\_dir
                /path/to/kivy\_instalation/kivy/tools/garden install --app graph
    
    This should install the Graph Widget in `my_app_dir/libs/garden/garden.widgetname`
    

Guide for migrating flowers from legacy structure
-------------------------------------------------

This is a guide for how to migrate a flower with legacy `garden.flower` structure to the new proper python package `flower` structure.

*   Demo of the result of converting **pure-python** graph from [legacy](https://github.com/kivy-garden/garden.graph) to [updated](https://github.com/kivy-garden/graph).
*   Demo of the result of converting **cython-python** collider from [legacy](https://github.com/kivy-garden/garden.collider) to [updated](https://github.com/kivy-garden/collider).

Here are the base [pure-python](https://github.com/kivy-garden/flower/) and [cython-python](https://github.com/kivy-garden/cython_flower) flowers to be used as starting points for the migration.

The following steps use the garden graph package to demonstrate how to migrate a package to the new format.

1.  Ensure that the original flower issues and pull requests are closed or can be closed because the repo will be archived after the following process. Issues can be transferred to the new repo if needed.
    
2.  Create a new empty repo with the name `graph` in [garden](https://github.com/kivy-garden/) or request in a new issue that we create one for you and give you access.
    
3.  In [coveralls](https://coveralls.io) sync the `kivy-garden` repos and then enable it (or request that we enable it).
    
4.  Clone the flower demo repo, if you haven't already. Otherwise make sure it is up to date with master: For a pure python flower: `sh git clone git@github.com:kivy-garden/flower.git` or for a cython-python flower: `sh git clone git@github.com:kivy-garden/cython_flower.git`
    
5.  Push the flower repo to github: `sh cd flower git push --mirror git@github.com:kivy-garden/graph.git`
    
6.  Now clone `graph` and the original `garden.graph` locally: `sh git clone git@github.com:kivy-garden/graph.git git clone git@github.com:kivy-garden/garden.graph.git`
    
7.  Merge `garden.graph` into the new `graph`:
    
        cd graph
                    git remote add original ../garden.graph
                    git remote update
                    git merge --allow-unrelated-histories original/master
                    
    
    If there are any merge conflicts, resolve them and commit.
    
8.  Migrate the original package structure into a pythonic structure.
    
    1.  Remove the `kivy-garden/flower` directory and make a new `kivy-garden/graph` directory.
    
    4.  Copy all the original python modules e.g. `__init__.py` into `kivy-garden/graph`.
    
    7.  Fix the tests in `tests/` to test the graph code.
    
    10.  open `setup.py` and replace all instances of `flower` with `graph`.
    
    13.  Do any remaining cleanup, e.g. duplicate license files or readme.
    
    16.  Commit all changes.
    

11.  Test to make sure everything works, otherwise fix and commit (make sure `pytest` is installed). Test install it to python and use it in your app: `sh pip install . python -c "from kivy_garden.graph import Graph"` If it's a cython flower (graph isn't), compile it first: `sh PYTHONPATH=.:$PYTHONPATH python setup.py build_ext --inplace` Then run the tests: `sh PYTHONPATH=. python -m pytest tests/`
    

14.  Push to kivy-garden and remove the original garden remote `sh git push origin master git remote rm original`
    

17.  Verify that the travis tests pass.
    

20.  Transfer issues from the `garden.graph` to `graph` and archive `garden.graph`.