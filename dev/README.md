This is a docker-compose configuration to be used **only** for development purpose.

## List of URLS

- Application: http://localhost:8000
- Dev Backend/API: http://localhost:8000/api/
- Dev Frontend: http://localhost:8001

## List of containers

### zimplorer

This container is the full application (UI + API), close to the real production container.

Python code is mounted inside the container and hot-reloaded (i.e. API development can be tested on this).

UI is statically compiled, so changes are not refreshed, use the frontend-tools UI for testing UI changes.

### backend-tools

This container is simply a Python stack with all backend requirements (including qa) but no web server.

It is used to run tests, etc ...

### frontend-tools

This container hosts the development frontend UI (i.e. `yarn dev`).

It is not the statically compiled version, so it is very usefull to test UI changes locally.

### Restart the application

The application might fail, typically if you create some nasty bug while modifying the code.

Restart it with:

```sh
docker restart zp_zimplorer
```

Other containers might be restarted the same way.

### Run tests

Run all tests with coverage report:

```sh
docker exec -it zp_backend-tools invoke coverage
```

You can select one specific set of tests by path

```sh
docker exec -it zp_backend-tools invoke test --path "unit/business/indicators/test_indicators.py"
```

Or just one specific test function

```sh
docker exec -it zp_backend-tools invoke test --path "unit/business/indicators/test_indicators.py" --args "-k test_no_input"
```