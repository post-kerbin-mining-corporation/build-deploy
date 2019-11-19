# Package Testing

To try to catch most of my common pitfalls with packaging mods, I have implemented some automated tests that run when a pull request is initiated. A 'build failed' message will be displayed if these failed.

## Check for missing dependencies

Tests the list of dependencies in the packages and ensures they all exist

## Check for uncompressed textures

All textures should be shipped in .png or .dds format, so a test runs to ensure that no .tga intermediates exist.

## Check for unused bumpmaps

Typically my artistic workflow involves bumpmaps in an interim stage. Sometimes I forget to delete these, so a test runs to verify that no files that end in `-b` exist.


# Future Tests

I'll write these sometime

## Check versioning

Checks that the `.version` file being merged contains a mod version that:

* Is not an existing tag
* Does not exist on SpaceDock or CurseForge

## Check KSP versioning

Checks that the `.version` file being merged targets a KSP version that exists on SpaceDock and CurseForge