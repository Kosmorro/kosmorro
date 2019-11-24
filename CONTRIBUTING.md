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

## Writing code

First of all, if you are fixing an opened issue, check that nobody is already working on it — if someone seems to be but their Pull Request seems stuck, please ask them first if you can continue the development. If you retake the code they produced, **don't change the author of the commits**.

Before writing the code, first create a fork of the repository and clone it. You may also want to add the original repository (`Deuchnord/kosmorro`), so you can update your fork with the last upstream commits.
Then create a new branch and start coding. Finally, commit and push, then open a PR on this project. If your project is not complete, feel free to open it as Draft (if you forgot to activate the Draft status, just edit the first comment to say it), then mark it as ready for review when you're done.

### Matching the coding standards

Kosmorro's source code follows the major coding standards of Python (PEPs). Before marking your Pull Request as ready for review, don't forget to check that the code respects the coding standards with PyLint (it is run on the CI, but feel free to run it on your local machine too). Your PR must have a global note of 10/10 to be elligible to merge.

### Testing the code

Sadly, Kosmorro currently has a poor code coverage, but feel free to add new unit tests to enhance its stability.
Any new Pull requests should have at least one new unit test that checks the new development is correct.

### Commiting

The commit messages of this project follow the [Conventional Commits Specification](https://www.conventionalcommits.org/en/v1.0.0/): basically, when you commit your changes, please prefix them with the following:

- **`fix: `** if your changes fix a bug;
- **`feat: `** if your changes add a new feature.

The message of your commit must start with a lowercase.
Finally, if your change introduce a BC-break, add an exclamation mark (`!`) before the colon.

Once your PR is ready to review, please squash your commits so it contains only one commit.

The commit messages are then used to generate the changelog using [`conventional-changelog`](https://github.com/conventional-changelog/conventional-changelog):

```bash
conventional-changelog -p angular -i CHANGELOG.md -s
```

## Licensing and Copyright Attribution

When you open a Pull Request to the project, you agree to license your code under the [GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html).
