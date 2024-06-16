# RatesTask

- [Overview](#Overview)<br/>
- [Running App with Docker](#Running-App-with-Docker)<br/>
- [Setting up App locally](#Setting-up-App-locally)<br/>
- [Notes](#Notes)<br/>

## Overview
This is a simple REST API which provides capabilities to show average price for each day for given origin to destination of freight.

#### Input

```json
date_from
date_to
origin
destination
```

#### Output
```json
[
    {
        "day": "2016-01-01",
        "average_price": 1112
    },
    {
        "day": "2016-01-02",
        "average_price": 1112
    },
    {
        "day": "2016-01-03",
        "average_price": null
    }
]
```

#### 1. System Requirements

```shell
python 3.11
```

#### 2. Install Requirements

```shell
make setup
```


