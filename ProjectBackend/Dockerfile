# Use an official Ubuntu image
FROM ubuntu:20.04

# Set the working directory in the container
WORKDIR /app

# Install required packages and tools
# Install required packages and tools
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get update \
    && apt-get install -y \
    python3.12 \
    python3.12-distutils \
    libreoffice \
    pandoc \
    wkhtmltopdf \
    && apt-get clean

# Set up a symlink for python3 to point to python3.12
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1

# Register GPG key and installation source for MiKTeX
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys D6BC243565B2087BC3F897C9277A7293F59E4889 \
    && echo "deb http://miktex.org/download/ubuntu focal universe" | tee /etc/apt/sources.list.d/miktex.list \
    && apt-get update

# Install MiKTeX
RUN apt-get install -y miktex \
    && miktexsetup finish


# Enable automatic package installation
RUN initexmf --set-config-value [MPM]AutoInstall=1

# Copy the current directory contents into the container at /app
COPY . /app

# Install pip for Python 3.12
RUN apt-get install -y python3.12-distutils \
    && wget https://bootstrap.pypa.io/get-pip.py \
    && python3.12 get-pip.py \
    && rm get-pip.py

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Command to run your application
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]