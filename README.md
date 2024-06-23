# RatesTask

- [Overview](#Overview)<br/>
- [Running App with Docker](#Running-App-with-Docker)<br/>
- [Setting up App locally](#Setting-up-App-locally)<br/>
- [Run unit tests locally](#Run-unit-tests-locally)<br/>
- [Database Schema](#Database-Schema)<br/>
- [Notes](#Notes)<br/>

## Overview
This is a simple REST API that provides the capability to show the average price for each day for a given origin to destination of freights. 
The following user stories are covered by the app:

* As a user, I want to query the average price of freights for a given origin and destination.
* As a user, I should be able to get the average price by passing either a port code or region slug for the origin and destination, and vice-versa.
* As a user, I should be able to query for a given time range.
* As a user, I expect null to be returned when there are fewer than 3 prices present for a day on a given route.
* As a user, I expect to query without passing a date range. Then the API should consider the current date (today) for querying. 
(This provides more practicality of using the API - Additional feature)

#### Query Parameters
- date_from
- date_to
- origin
- destination

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

## Running App with Docker

#### 1. Build the image

```shell
docker compose build
```

#### 2. Run the services

```shell
docker compose up
```
Point your browser to [http://localhost:8015/swagger](http://localhost:8015/swagger) to access swagger UI.


## Setting up App locally

#### 1. System Requirements

```shell
python 3.11
```

#### 2. Install Requirements

```shell
make setup
```

#### 3. Set Environments variables

Environment variables needed to run the app
```shell
export DB_URL=<db-url>
```
DB URL should be in following format. Refer [this](https://docs.sqlalchemy.org/en/20/core/engines.html#postgresql)

## Run unit tests locally

```shell
make test-unit-ci
```

Test report location: [reports](reports)

## Database Schema
Here's the ER-diagram of the database.

![ER-Diagram.png](resources%2Fstatic%2FER-Diagram.png)

## Notes
* The API has been developed mostly for happy path flow. The probable improvements
  * Enable pagination for the get rates endpoint.
  * Although an ORM framework is used, its ORM features have not been utilized since the assignment requires raw SQL.
    (Therefore, model classes for database schema have not been implemented)
  
* Average price has been rounded to the nearest integer as the output of the example is expected to be an integer according to the sample response.