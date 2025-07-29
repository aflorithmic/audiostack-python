# How to contribute to this project

- Update CHANGELOG.md
- After you have committed your changes, update the version with `poetry version <patch/ minor/ major>` following semantic versioning.
- Then add a new tag with that version number: `git tag -a v$(poetry version --short)`.
- Finally push to github with `git push origin v$(poetry version --short)`


## Updating internal branch

The `internal` branch needs to stay updated with the `main` branch.  However, trying to merge will result in potential breaking changes and problems.  For most cases, we want to merge only the latest commit from `main` into `internal`.

If we want to apply a small number of commits to `internal`, we can use [Cherry Pick](https://betterstack.com/community/questions/how-to-selectively-merge-or-pick-changes-from-another-branch-in-git/).  This lets us apply only certain commits.  However, it can be potentially tricky to cherry pick a merge commit.  It is better to cherry pick individual commits, therefore this method is better suited to a small number of commits.

If you have a lot of commits, you can cherry pick a merge commit, but you have to specify which changes you want relative to the parents (your feature branch and main).  In most cases we only want changes introduced by our feature branch, which would be the 2nd branch.

### Steps

- Get latest main commit hash that you want to merge with internal
- Go to internal and type `git cherry-pick <commit hash>` or `git cherry-pick <commit hash> -m 2` if you are cherry picking a merge commit
- Resolve merge conflicts if necessary
- Make sure to add all files to stage changes (none should be in merge changes)
- Commit and push as normal
