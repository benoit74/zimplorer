FROM node:20-alpine as zimplorer_ui

WORKDIR /src
COPY frontend /src
RUN yarn install --frozen-lockfile
RUN VITE_BACKEND_ROOT_API="./api/v1" yarn build

FROM python:3.12-alpine
LABEL org.opencontainers.image.source https://github.com/offspot/metrics

# Specifying a workdir which is not "/"" is mandatory for proper uvicorn watchfiles
# operation (used mostly only in dev, but changing the workdir does not harm production)
WORKDIR "/home"

# Install necessary packages (only pip so far)
RUN python -m pip install --no-cache-dir -U \
      pip

ENV DATABASE_URL sqlite+pysqlite:////data/database.db

COPY backend/pyproject.toml backend/README.md /src/
COPY backend/src/zimplorer/__about__.py /src/src/zimplorer/__about__.py

# Install project dependencies
RUN pip install --no-cache-dir /src

# Copy code + associated artifacts
COPY backend/src /src/src
COPY backend/*.md /src/

# Install project + cleanup afterwards
RUN pip install --no-cache-dir /src \
 && cd /src/src \
 && rm -rf /src \
 && mkdir -p /data

COPY --from=zimplorer_ui /src/dist /src/ui

EXPOSE 80

CMD ["uvicorn", "zimplorer.entrypoint:app", "--host", "0.0.0.0", "--port", "80"]
