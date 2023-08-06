# dkist-processing-test

## Overview
The dkist-processing-test library serves as an example implementation of a Tasks and Workflows using the
[dkist-processing-core](https://pypi.org/project/dkist-processing-core/) framework and
[dkist-processing-common](https://pypi.org/project/dkist-processing-common/) Tasks.

The recommended project structure is to separate tasks and workflows into seperate packages.  Having the workflows
in their own package facilitates using the build_utils to test the integrity of those workflows in the unit test.
[example](dkist_processing_test/tests/test_workflows.py)

## Build
Artifacts are built through [bitbucket pipelines](bitbucket-pipelines.yml)

The pipeline can be used in other repos with a modification of the package and artifact locations
to use the names relevant to the target repo.

e.g. dkist-processing-test -> dkist-processing-vbi and dkist_processing_test -> dkist_processing_vbi

## Deployment
Deployment is done with [turtlebot](https://bitbucket.org/dkistdc/turtlebot/src/master/) and follows
the process detailed in [dkist-processing-core](https://pypi.org/project/dkist-processing-core/)

### Environment Variables
Only those specified by [dkist-processing-core](https://pypi.org/project/dkist-processing-core/) and [dkist-processing-common](https://pypi.org/project/dkist-processing-common/).

## Development

```bash
git clone git@bitbucket.org:dkistdc/dkist-processing-test.git
cd dkist-processing-test
pre-commit install
pip install -e .[test]
pytest -v --cov dkist_processing_test
```
