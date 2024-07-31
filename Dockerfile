# Stage 1: Build Stage
FROM python:3.11-alpine AS build


RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt

# Install dependencies
RUN apk --no-cache update && apk add postgresql-dev python3-dev uvicorn musl-dev build-base alpine-sdk \
    && pip install --upgrade pip \
    && pip install --prefix=/install --no-warn-script-location -r /requirements.txt \
    && find /install \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /install \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps

# Stage 2: Production Stage
FROM python:3.11-alpine AS production

# Install runtime dependencies
COPY --from=build /install /usr/local

RUN apk --no-cache add libpq libstdc++ gcc libgcc linux-headers uvicorn

# Set working directory
RUN mkdir /app
COPY . /app/
WORKDIR /app

# Install only necessary runtime dependencies
RUN pip install --upgrade pip

ENV PYTHONUNBUFFERED=0

# Command to run the FastAPI app
CMD ["sh", "-c", "tail -f /dev/null"]