[![PyPI version](https://badge.fury.io/py/gethue.svg)](https://badge.fury.io/py/gethue)
[![Test Status](https://github.com/gethue/compose/workflows/Python%20CI/badge.svg?branch=master)](https://github.com/gethue/compose/actions?query=Python%20CI)
[![DockerPulls](https://img.shields.io/docker/pulls/gethue/compose.svg)](https://registry.hub.docker.com/u/gethue/compose/)
![GitHub contributors](https://img.shields.io/github/contributors-anon/gethue/compose.svg)
[![Code coverage Status](https://codecov.io/gh/gethue/compose/branch/master/graph/badge.svg)](https://codecov.io/gh/gethue/compose)
[![License](https://img.shields.io/github/license/mashape/apistatus.svg)](https://pypi.org/project/gethue/)

<kbd><img src="https://raw.githubusercontent.com/gethue/compose/master/docs/images/compose_button.png"/></kbd>

Compose
-------

[Query Editor component](https://docs.gethue.com/developer/components/scratchpad/)

Compose is the open source module powering the [Hue SQL Editor](http://gethue.com). It comes as a Web service API for querying any [Databases & Data Warehouses](https://docs.gethue.com/administrator/configuration/connectors/) or building your own [Cloud SQL Editor](https://docs.gethue.com/developer/components/).


<img src="https://cdn.gethue.com/uploads/2021/05/sql-scratchpad-v0.5.png" width="450">


# Start

Hello World query

    curl -u hue:hue -X POST http://localhost:8005/editor/v1/query/sqlite --data 'statement=SELECT 100, 200'

Docker

    docker run -it -p 8005:8005 gethue/compose:latest

Pypi

    pip install gethue

    compose-admin migrate
    compose-admin createsuperuser
    compose-admin start

    compose auth
    compose query
    compose storage list s3a://demo-gethue

# Dev

One time

    git clone https://github.com/gethue/compose.git
    cd compose
    ./install.sh  # If you want a Python virtual-env
    pre-commit install

Start API

    source python_env/bin/activate
    python compose/manage.py runserver 0.0.0.0:8005

Config

    compose/conf/local_settings.py

Checks

    pre-commit run --all-files
    python compose/manage.py test

Hue

    npm run webpack-npm

# API

Live

* https://api.gethue.com/api/schema/swagger-ui/
* https://api.gethue.com/api/schema/redoc/

Query

    curl -u hue:hue -X POST http://localhost:8005/api/editor/execute/sqlite --data 'statement=SELECT 100, 200'

    curl -u hue:hue -X POST http://localhost:8005/api/editor/execute/sqlite --data 'statement=SELECT 100, 200'
    curl -u hue:hue -X POST http://localhost:8005/api/editor/check_status --data 'qid=abc'
    curl -u hue:hue -X POST http://localhost:8005/api/editor/fetch_result_data --data 'qid=abc'
