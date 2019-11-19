# Notes on Deployment

Here are a few notes on deployment providers and peculiarities.

## Changelogs

Changelogs are generated from `changelog.txt`. At the moment this is a fairly rigid process. A changelog should look like this exactly:

```
1.1.0
=====
- Changed some things
  - An indented thing 
  - An indented thing 2

1.0.0
=====
- First release
  - An indented thing 

```
The top entry will be used as the changelog for the current version, so here that would be parse to:

* Changed some things
  * An indented thing
  * An indented thing 2

This will be parsed into Markdown which all deployment providers can read properly.

## GitHub

When a PR is merged, the repository is tagged with that version number in order to create a release checkpoint. A new release is then cut on Github with the latest changelog as its description

## SpaceDock

The zip with changelog is uploaded to Spacedock. Deployment will fail if SpaceDock doesn't have the KSP version yet.

## CurseForge

Nothing special, but as CF updates its KSP version so slowly, the deployment will always tag with the latest KSP version CF has aviailable instead of waiting. 
