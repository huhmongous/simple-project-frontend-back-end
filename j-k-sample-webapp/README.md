# Dead-Simple Webapp

## Description

This is an extremely bare-bones, simple webapp that demonstrates the entire full-stack involved in implementing a webapp from scratch.

### Architecture

* There is a containerized Python app that provides a basic JSON API with dynamic data returns.
* There is an nginx configuration that can be loaded by the official nginx container image to act as a reverse proxy for the Python app containers.
* There is a static webpage acting as a frontend client to the backend API, making requests to the API via the nginx proxy, and displaying the output to the user.

## Usage

### Building the backend containers

From the repository root directory, run the following command to build the backend app container image:

```
docker build -t jk_simple_backend .
```

### Running the containers

We use a standard Docker bridge network to allow the containers to communicate. Ensure you've created the bridge network `testapp` before running the containers:

```
docker network create testapp
```

Start the backend webapp containers:

```
docker run -d --network testapp --name app_server_1 -e SERVER_ID=1 jk_simple_backend
docker run -d --network testapp --name app_server_2 -e SERVER_ID=2 jk_simple_backend
```

Once the backend containers are running, start the nginx reverse proxy:

```
docker run --rm -d --network testapp -p 8080:80 -v $(pwd)/conf/nginx.conf:/etc/nginx/nginx.conf:ro nginx
```

### Testing the app

Load up the `src/index.html` file in your favorite browser, then click the "Run!" button. You should see the response JSON from the `/server` API endpoint displayed in the div element below the text field and button. It should alternate between an ID value of 1 or 2, depending on which backend app container handled the HTTP request.

## Links

* [FastAPI](https://fastapi.tiangolo.com/)
* [Uvicorn](https://www.uvicorn.org/)
* [nginx Container](https://hub.docker.com/_/nginx)
* [FastAPI-Uvicorn Container](https://hub.docker.com/r/tiangolo/uvicorn-gunicorn-fastapi)
* [Axios](https://axios-http.com/docs/intro)

## Next Steps

Suggestions for improving this basic webapp and getting a better feel for how everything works:

* Add an additional backend container to the worker pool. Make sure to modify the upstream configuration in nginx to route traffic to it.
* Add a "start everything" script that starts the backend app containers and the proxy with a single command.
* Add a `build.sh` script to build the backend app container without needing to remember or look up the correct Docker build stanza.
* Add a new API endpoint that does something beyond merely returning static (or simplistic) data. Integrate it with the frontend.
  * Random number generator -- Have it accept different parameters that control the type of random number it generates and returns
  * Password generator -- Find a simple password generation library (if nothing suitable exists in the standard library) and generate random passwords. Parameters passed can control whether to use special characters, etc.
  * QR code generator -- Take text input, encode it as a QR code, return that QR code image base64 encoded, display the QR code as an image to the user in the frontend client
  * Data search -- Add a data file to each of the backend app containers, via the build process, and have a new endpoint search through that file based on a search key that the user provides.
  * Integrate with an external RDBMS
    * Use the [Postgres container](https://hub.docker.com/_/postgres) to keep things local and simple
  * Integrate with an external Redis cache
    * [Official Redis container instructions](https://redis.io/docs/stack/get-started/install/docker/)