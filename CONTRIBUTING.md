# Contributing to Kosmorro

If you are reading this, then you are probably looking for a way to contribute to Kosmorro (you're in the good place!). Thank you!
There are multiple ways to contribute that can match with your possibilities.

## Opening issues

### Reporting bugs

If you found a bug, please check it is not already reported in the _Issues_ tab.
If it is not, [create a bug report](https://github.com/Deuchnord/kosmorro/issues/new/choose) and fill in the template that offers to you. Feel free to give as much information as possible, as it will make the bug easier to fix.

### Suggest a new feature

Have an idea of feature you think would be nice on Kosmorro? Time to suggest it!
First, please check someone didn't suggest your next revolution in the _Issues_ tab. If it's not, [create a feature request](https://github.com/Deuchnord/kosmorro/issues/new/choose) and fill in the templace that offers to you.

## Translating

If you speak another language than English, another nice way to enhance Kosmorro is to translate its messages. The recommended way to begin translating Kosmorro is to [join the Weblate project](https://hosted.weblate.org/engage/kosmorro/).

## Writing code

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/Kosmorro/kosmorro)

First, if you are fixing an opened issue, check that nobody is already working on it — if someone seems to be but their Pull Request seems stuck, please ask them first if you can continue the development. If you retake the code they produced, **don't change the author of the commits**.

Before writing the code, first create a fork of the repository and clone it. You may also want to add the original repository (`Kosmorro/kosmorro`), so you can update your fork with the last upstream commits.

Then create a new branch and start coding. Finally, commit and push, then open a PR on this project. If your project is not complete, feel free to open it as Draft, then mark it as ready for review when you're done.

### Choosing the right target branch

Whatever you are doing, always base your working branch on `master`.
When you create your PR, please consider selecting the right target branch:

- If you are fixing a bug or optimizing something, then target the `master` branch.
- If you are doing anything else, then target the `features` branch.

This allows to make easier to publish patch releases, which have a higher priority than the minor releases.

### Dealing with the translations

The messages file contains all the messages Kosmorro can display, in order to make them translatable. When you change code, you may change also the messages displayed by the software.

When you add a new string that will be displayed to the end user, please pass it to the `_()` function made available in the `kosmorrolib.i18n` package, for instance:

```python
# Don't:
print('Note: All the hours are given in UTC.')

# Do:
from kosmorro.i18n import _
print(_('Note: All the hours are given in UTC.'))
```

This will allow Python's internationalization tool to translate the string in any available language.

Once you have done your work, please remember to tell [Babel](http://babel.pocoo.org) to extract the new strings:

```bash
make messages
```

Note that if you forget to update the messages file, the CI will fail.

### Matching the coding standards

Kosmorro's source code follows the major coding standards of Python (PEPs).
Before marking your Pull Request as ready for review, don't forget to check that the code respects the coding standards with Black:

```bash
make black
```

### Testing the code

The tests are located in the `/tests` folder.
Their principle is pretty simple:

1. First, we run a Kosmorro command as we would in command line application. We use the [Aurornis](https://pypi.org/project/aurornis/) package to do this.
2. Then, we test the return of the command against what we expected. We use [PyTest](https://pypi.org/project/pytest/) to do this.

To run the tests, invoke the following command:

```bash
make tests

# Or, if you have TeXLive installed on your machine (Linux only):
make TEXLIVE_INSTALLED=1 tests
```

### Commiting

The commit messages of this project follow the [Conventional Commits Specification](https://www.conventionalcommits.org/en/v1.0.0/): basically, when you commit your changes, please prefix them with the following:

- **`fix: `** if your changes fix a bug;
- **`feat: `** if your changes add a new feature.

The message of your commit must start with a lowercase.
Finally, if your change introduce a BC-break, add a footer beginning with `BREAKING CHANGE:` and explaining precisely the BC-break.

Once your PR is ready to review, please squash your commits so it contains only one commit.

> To ensure your commits follow this convention, you can use [glint](https://github.com/brigand/glint).

The commit messages are then used to generate the changelog using [`conventional-changelog`](https://github.com/conventional-changelog/conventional-changelog).

## Licensing and Copyright Attribution

When you open a Pull Request to the project, you agree to license your code under the [GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html).
