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

# Clone the repository
RUN git clone https://github.com/727yubin/easy_grading.git

# Change working directory
WORKDIR /easy_grading

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

# Expose the port
EXPOSE 8080

# Run the application with Waitress
CMD ["waitress-serve", "--port=8080", "app:app"]

