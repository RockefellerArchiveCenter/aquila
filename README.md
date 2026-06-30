# aquila

An application to store, calculate, and assign PREMIS rights statements.

## Getting Started

Install [git](https://git-scm.com/) and clone the repository

    $ git clone https://github.com/RockefellerArchiveCenter/aquila.git

Install [Docker](https://store.docker.com/search?type=edition&offering=community) and run docker-compose from the root directory

    $ cd aquila
    $ docker compose up

When you're done, shut down docker-compose

    $ docker-compose down

Or, if you want to remove all data

    $ docker-compose down -v

## Authentication

This application uses Microsoft Entra to manage users. In order to successfully log in, you will need several variables, which should be provided to the application as environment variables:
- `MS_APP_ID` - ID of the configured Microsoft Entra app.
- `MS_APP_SECRET` - Secret key for the configured Microsoft Entra app
- `MS_APP_AUTHORITY` - Authentication endpoint

Additional configurations are available. See the `docker-compose.yml` file for these configurations and their default values.

## Usage

Aquila includes a front-end interface to create rights statements and groupings, as well as an API to assemble rights statements.

Groupings are groups of content that have similar rights. They may correspond to record types, collections, or projects.

The rights statements contain date rules that are calculated by the Rights Assembler API. Many rights statements can be attached to many groupings.

### API

Aquila contains a Rights Assembler API (available at `api/rights-assemble/`), which uses a start date, an end date, and IDs of rights statements to create rights JSON.

## Requirements

Using this repo requires having [Docker](https://store.docker.com/search?type=edition&offering=community) installed.

## Development

This repository contains a configuration file for git [pre-commit](https://pre-commit.com/) hooks which help ensure that code is linted before it is checked into version control. It is strongly recommended that you install these hooks locally by installing pre-commit and running `pre-commit install`.

## License

Code is released under an MIT License, as all your code should be. See [LICENSE](LICENSE) for details.
