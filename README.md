Shippy - The docker builderoo
=============================

A tool to build and provision a docker-compose stack for a webapp given an application commit hash. Built using [pybuilder](http://pybuilder.github.com)

  - [Project dependencies](#project-dependencies)
  - [Setup](#setup)
    - [Python3](#python3)
    - [Docker](#docker)
    - [Pybuilder](#pybuilder)
  - [Installation](#installation)
  - [Usage](#usage)


# Project dependencies

* Python 3.5 or later
* [pybuilder](http://pybuilder.github.io)
* [Requests](https://github.com/requests/requests)
* [Docker-py](https://docker-py.readthedocs.io/en/stable/)
* [tqdm](https://github.com/noamraph/tqdm)
* [validictory](https://github.com/jamesturk/validictory)
* [argh](https://readthedocs.org/projects/argh/)
* [jinja2](http://jinja.pocoo.org/)


# Supported Platforms

This project was build using python3.6 and Docker for mac version 17.06.0-ce, on macOS Sierra.
It should work on any unix-like platform that docker supports but has not been tested on any other
platforms yet. *NOT* supported on Windows.


# Setup

## Python 3

For macOS, the best way to install python 3 is via [homebrew](https://brew.sh/), make sure its installed correctly
and configured properly by running `brew doctor`, ensuring there are no errors.

To install python3 via homebrew:

`brew install python3`

## Docker

To install docker for your platform, please follow the [official installation instructions](https://docs.docker.com/engine/installation/)

## Pybuilder

Once you have got python3 and docker installed and working in your environment, install pybuilder
by running:

`pip install pybuilder`


# Installation

With a working pybuilder installation, you are now ready to run the pybuilder tasks defined
in the project:

From the root of the repository, run: `pyb`, this command will:
* Install dependencies
* Run linting and unittests
* Build an installable package

To install the tool you can then run `pyb install`


# Usage

Installing shippy should now expose the `shippy_deploy` command:

```bash
shippy_deploy -h
usage: shippy_deploy [-h] configpath appconfig sha

    Deploys an application stack


positional arguments:
  configpath  Path to build config
  appconfig   Path to application config
  sha         Commit hash to build source from

optional arguments:
  -h, --help  show this help message and exit
```

```bash
shippy_deploy myconfig.json  ghost_config.js --sha 827aa15757bcfdcfe7cbb0a3ce9e3c3117657ce2
```

To deploy a new application stack, you will need:
* Build config file
* Application config file
* Commit hash

There is an example in the [examples](examples/ghost) folder for the [ghost blogging platform](https://github.com/TryGhost/Ghost).

## Build Configuration

The build configuration is used to define the stack configuration, as an example:

build_ghost.json
```json
{
  "application_image": "thedigitalgarage/ghost",
  "application_repository": "https://github.com/tryghost/ghost",
  "application_source_mountpoint": "/usr/src/ghost",
  "application_config": {
    "GHOST_URL": "http://www.example.com",
    "NODE_ENV": "production",
    "GHOST_SOURCE": "/usr/src/ghost",
    "DB_CLIENT": "mysql",
    "DB_USER": "ghost_user",
    "DB_PASSWORD": "ghostadmin1234",
    "DB_HOST": "db"
  },
  "application_build_cmds": [
    "npm install --production"
  ],
  "database_image": "mysql/mysql-server",
  "database_config": {
    "MYSQL_USER": "ghost_user",
    "MYSQL_PASSWORD": "ghostadmin1234",
    "MYSQL_DATABASE": "ghost",
    "MYSQL_ROOT_PASSWORD": "admin1234"
  }
}
```

* `application_image`: The docker image to use for the application
* `application_repository`: Github repository for the application
* `application_source_mountpoint`: The mountpoint to mount the application source at
* `application_config`: Docker env vars to pass to your application container
* `application_build_cmds`: Commands to run to build to build your source
* `database_image`: Docker image to use for your database
* `database_config`: Docker env vars to pass to your database container


# Design Considerations

There are a few different ways to build an application stack from a given commit hash:

1. Build a custom Dockerfile for the application to pull down source given a SHA from the 
github release API
2. Use a build container to build a stripped down application container
3. Create a data volume containing the sourcecode for the given SHA, and then mount the volume
at the target mountpoint in the application container

Shippy is built using option 3. The following sequence of events occur when `shippy_deploy` is
executed.


1. Download archive tarball from github archive API for the given SHA
2. Unpack archive (removing the nested top-level folder)
3. Run the build command (this requires build tools to be installed on the host)
4. Copy config template into root of the expanded source directory
5. Put a generated Dockerfile into the root of the expanded source directory
6. Build a docker data image, copying in this source directory at the desired volume mountpath, and exporting it
7. Put a generated docker-compose.yml file in the root of the expanded source directory
8. Run `docker-compose -p <app_name>_<sha> up -d` from the source directory


# Accessing Containers by Hostname

By default you would have to access the containers by port, if they are exposed on the host,
but you can use the [DNS proxy server container](https://github.com/mageddo/dns-proxy-server) 
which would listen to the docker socket and automatically add hosts entries.


1. Start the DNS proxy container

```bash
$ docker run --hostname dns.mageddo --name dns-proxy-server -p 5380:5380 \
-v /var/run/docker.sock:/var/run/docker.sock \
-v /etc/resolv.conf:/etc/resolv.conf \
defreitas/dns-proxy-server
```

2. The application stack will define a hostname for your application with the following format:

```bash
<application_name>_<sha>.dev.internal
```
 
When the stack is up, running `nslookup` should return a result:
 ```bash
 $ nslookup ghost_b37411239f70f538e198e238610a0e7e9c6b83b0.dev.internal
 Server:     172.17.0.2
 Address:    172.17.0.2#53
 
 Non-authoritative answer:
 Name:   ghost_b37411239f70f538e198e238610a0e7e9c6b83b0.dev.internal
 Address: 172.21.0.3
```
NB - It should also resolve DNS to non-docker hostnames as normal

```bash
$ nslookup google.com
Server:     172.17.0.2
Address:    172.17.0.2#53

Non-authoritative answer:
Name:   google.com
Address: 216.58.202.78
```

# Roadmap

Currently shippy only supports creating new application stacks, in future releases support
will be added for:

* Listing all running stacks (with hostnames)
* Destroy a stack
* Updating a running stack


# License

Licensed under [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html)


# Author

Vik Bhatti (github@vikbhatti.com)
