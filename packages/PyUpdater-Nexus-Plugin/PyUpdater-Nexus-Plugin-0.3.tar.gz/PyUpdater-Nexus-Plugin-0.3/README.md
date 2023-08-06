[![PyPI version](https://badge.fury.io/py/PyUpdater-Nexus-Plugin.svg)](https://badge.fury.io/py/PyUpdater-Nexus-Plugin)

# PyUpdater Nexus plugin

PyUpdater upload plugin for Nexus sonatype instance.
Uses a raw repository for storing files

## Installing

    $ pip install PyUpdater-Nexus-plugin


## Configuration

System environmental variables

Optional - If set will be used globally. Will be overwritten when you add S3 settings during pyupdater init

| Env Var               | Meaning                                 |
| --------------------- |---------------------------------------- |
| PYU_NEXUS_URL         | URL of Nexus instances                  |
| PYU_NEXUS_PASSWORD    | HTTP basic auth password                |
| PYU_NEXUS_USERNAME    | HTTP basic auth username                |
| PYU_NEXUS_REPOSITORY  | Repository name                         |
| PYU_NEXUS_DIRECTORY   | Directory from repository               |
