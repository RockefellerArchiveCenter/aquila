# aquila

[![Build Status](https://travis-ci.com/RockefellerArchiveCenter/aquila.svg?branch=base)](https://travis-ci.com/RockefellerArchiveCenter/aquila)

An application to store, calculate, and assign PREMIS rights statements.

## Getting Started

Install [git](https://git-scm.com/) and clone the repository

    $ git clone https://github.com/RockefellerArchiveCenter/aquila.git

Install [Docker](https://store.docker.com/search?type=edition&offering=community) and run docker-compose from the root directory

    $ cd aquila
    $ docker-compose up

A default user with username `test` and password `testpassword` is created on setup. Once the application starts successfully, you should be able to access the application in your browser at `http://localhost:8000`.

When you're done, shut down docker-compose

    $ docker-compose down

Or, if you want to remove all data

    $ docker-compose down -v


## Default Superuser

When you start the container for the first time, a superuser will be created. Make sure you change the password for this user (the easiest way is through the Django shell). E.g.,

```
python manage.py changepassword <SUPERUSER_USERNAME>
```

## Usage

Aquila includes a front-end interface to create rights statements and groupings.

Groupings are groups of content that have similar rights. They may correspond to record types, collections, or projects.

Many rights statements can be attached to many groupings.

## Requirements

Using this repo requires having [Docker](https://store.docker.com/search?type=edition&offering=community) installed.

## Development

This repository contains a configuration file for git [pre-commit](https://pre-commit.com/) hooks which help ensure that code is linted before it is checked into version control. It is strongly recommended that you install these hooks locally by installing pre-commit and running `pre-commit install`.

## License

Code is released under an MIT License, as all your code should be. See [LICENSE](LICENSE) for details.
