# How to contribute to this project

- Update CHANGELOG.md
- After you have committed your changes, update the version with `poetry version <patch/ minor/ major>` following semantic versioning.
- Then add a new tag with that version number: `git tag -a v$(poetry version --short)`.
- Finally push to github with `git push origin v$(poetry version --short)`
