# issue-tracker
Calculate time statistics from HUNTeR issues

## Basic usage

Clone this repository and run `./make-stats.py https://api.github.com/repos/SBI-/minimal-git-api/issues` from the issue-tracker folder. The URL needs to point to the issues api endpoint of any repository you wish to create statistics for.

## Authentication
If you wish to run the issue tracker on a private repository, create a file called `secret_token` in this folder, containing a GitHub personal access token. This token will be used to fetch the private repository.
