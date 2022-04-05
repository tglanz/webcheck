# python-request-interception

## Personal notes

Goals I had in mind are to enable future changes and decoupling concepts.

One issue I have is with the form of how the backend routes are set up. First time making rest APIs with flask so the result was not the most elegant.

## Running the server

(Optional) Create a python virtual environment and activate it

    python -m venv .venv

    source .venv/bin/activate

Start the server which will bind to port 5000 (by default)

    python backend/server.py

## Running an example code

(Optional) Create a python virtual environment and activate it

    python -m venv .venv

    source .venv/bin/activate

Run the examples

    PYTHONPATH=. python examples/simple.py
    PYTHONPATH=. python examples/app.py --url http://www.google.com

## Backend API

> Note: Some terminologies and arrangements are a bit of. I used initially the flask resources, and they confine a bit.

Get all request details - ```GET api/v1/requests/get```

    curl localhost:5000/api/v1/requests/get

Get request details by id - ```GET api/v1/requests/get?id={id}```

    curl localhost:5000/api/v1/requests/get?id=e9717796-bb7d-4b22-9f56-07fec838d4c5

Get the most frequent website - ```GET api/v1/requests/frequent-website```

    curl localhost:5000/api/v1/requests/frequent-website

Get all requests in a specified time frame ```GET api/v1/requests/time-frame?from={from-iso-time}&to={to-iso-time}```

    curl "localhost:5000/api/v1/requests/time-frame?from=2022-04-05T23:00:00&to=2022-04-05T23:24:04"
    

## Further Improvement

- Tests
- Better error handling
- Async IO when contacting webcheck servers
- Splitting requests for "RequestBegin" "RequestCompleted". Currently we cannot detect crashes since we only record upon completion
- Relational storage was chosen for simplicity, perhaps different solutions are preferable
- Backed can be greately improve design wise. The backend should support unknown workloads. Natural improvements
    1. Multiple instances behind a load balancer
    1. Insert requests into a queue and have a cluster of workers handle them