FROM alpine:latest

# Install required packages and dependencies
RUN apk update && \
    apk add --no-cache \
    python3 \
    py3-pip \
    git \
    build-base \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    tk-dev \
    tcl-dev \
    libxslt-dev \
    libxml2-dev \
    libffi-dev \
    libjpeg-turbo-dev \
    libpng-dev \
    libwebp-dev \
    gcc \
    musl-dev

# Install Python dependencies
RUN pip3 install --no-cache-dir --break-system-packages\
    Flask \
    Flask-Login \
    Flask-SQLAlchemy \
    Flask-Session \
    psycopg2-binary \
    flask-cors \
    pandas \
    qrcode \
    Pillow \
    werkzeug \
    numpy \
    reportlab \
    waitress


