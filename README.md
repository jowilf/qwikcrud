# qwikcrud

[![PyPI - Version](https://img.shields.io/pypi/v/qwikcrud.svg)](https://pypi.org/project/qwikcrud)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/qwikcrud.svg)](https://pypi.org/project/qwikcrud)

-----

QwikCrud is a powerful command-line tool designed to revolutionize your backend development experience by automating the
generation of comprehensive RESTful APIs and admin interfaces. Say goodbye to the tedious task of
writing repetitive CRUD (Create, Read, Update, Delete) endpoints when starting a new project, allowing developers to
concentrate on the core business logic and functionality.

> **⚠️ Warning**
> While the generated application works fine, it is not ready for production use. Additional steps are required to
> set up a secure and production-ready environment.


[![Qwikcrud demo](https://github.com/jowilf/qwikcrud/assets/31705179/fc010d41-597c-4ab7-a0ad-22570ba3b182)](https://vimeo.com/889381304 "Qwikcrud demo - A restaurant management app")

## Table of Contents

* [Installation](#installation)
* [Quickstart](#quickstart)
    * [Environment variables](#environment-variables)
    * [Usage](#usage)
    * [Generated Application stack](#generated-application-stack)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [Acknowledgments](#acknowledgments)
* [License](#license)

## Installation

```shell
pip install qwikcrud
```

## Quickstart

### Environment variables

Before running the command-line tool, ensure the following environment variables are configured:

```shell
export OPENAI_API_KEY="your_openai_api_key"
export OPENAI_MODEL="your_openai_model" # Defaults to "gpt-3.5-turbo-1106"
```

### Usage

To generate your application, open your terminal, run the following command and follow the instructions:

```shell
qwikcrud -o output_dir
```

### Generated Application stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy v2](https://www.sqlalchemy.org/)
- [Pydantic v2](https://docs.pydantic.dev/latest/)
- [Starlette-admin](https://github.com/jowilf/starlette-admin)
- [SQLAlchemy-file](https://github.com/jowilf/sqlalchemy-file)

## Roadmap

QwikCrud is designed to support various stacks and AI providers. Here's an overview of what has been accomplished and
what is planned for the future:

- [x] FastAPI + SQLAlchemy
    - [x] CRUD Endpoints
    - [x] Admin interface with Starlette-admin
    - [x] File Management with SQLAlchemy-file
    - [ ] Authentication
- [ ] FastAPI + Beanie
- [ ] SpringBoot
- [ ] Local LLMs support.

## Contributing

Contributions are welcome and greatly appreciated! If you have ideas for improvements or encounter issues, please feel
free to submit a pull request or open an issue.

## Acknowledgments

- The FastAPI + SQLAlchemy template is inspired by the excellent work
  in [full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql)
  by [Sebastian Ramirez (tiangolo)].

## License

`qwikcrud` is distributed under the terms of the [Apache-2.0](https://spdx.org/licenses/Apache-2.0.html) license.