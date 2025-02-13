# How to contribute to this project

- Update CHANGELOG.md
- After you have committed your changes, update the version with `poetry version <patch/ minor/ major>` following semantic versioning.
- Then add a new tag with that version number: `git tag -a v$(poetry version --short)`.
- Finally push to github with `git push origin v$(poetry version --short)`


## Updating internal branch

The `internal` branch needs to stay updated with the `main` branch.  However, trying to merge will result in potential breaking changes and problems.  For most cases, we want to merge only the latest commit from `main` into `internal`.

I found a nice way to do what we want [Cherry Pick](https://betterstack.com/community/questions/how-to-selectively-merge-or-pick-changes-from-another-branch-in-git/)

### Steps

- Get latest main commit hash that you want to merge with internal
- go to internal and type `git cherry-pick <commit hash>`
- resolve merge conflicts if necessary
- make sure to add all files to stage changes (none should be in merge changes)
- commit and push as normal