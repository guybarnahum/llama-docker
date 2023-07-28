# using ubuntu LTS version
# (mostly to get latest gxx-9 build tools needed for llama.cpp)
FROM ghcr.io/abetlen/llama-cpp-python:latest

# install requirements
RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*

#RUN wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-MacOSX-arm64.sh && \
#    bash Miniforge3-MacOSX-arm64.sh

COPY requirements.txt .

RUN pip3 install --force-reinstall --upgrade --no-cache-dir wheel
#  -DLLAMA_METAL=On
RUN CMAKE_ARGS="-DBUILD_SHARED_LIBS=On" FORCE_CMAKE=1 \
    pip3 install --force-reinstall --upgrade --no-cache-dir llama-cpp-python[server]
RUN pip3 install --force-reinstall --upgrade --no-cache-dir -r requirements.txt

RUN mkdir /code
WORKDIR /code

# COPY . .
# either download models into image or mount the images from host (in dev)
#RUN python3 ./scripts/download_models.py

EXPOSE 8000

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1
    
COPY fastapi-server.py .
CMD ["python3", "fastapi-server.py"]