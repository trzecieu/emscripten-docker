ARG EMSCRIPTEN_SDK=sdk-tag-1.38.25-64bit
FROM trzeci/emscripten:${EMSCRIPTEN_SDK} as emscripten_base

# ------------------------------------------------------------------------------
# Entries in this section is required to move Emscripten SDK to another base image

# This can be any base image
FROM ubuntu:bionic

# Source /emsdk_portable should be contain every emscripten tool.
# It's not recommended to change destination location
COPY --from=emscripten_base /emsdk_portable /emsdk_portable

# Emscripten to operate requires EMSDK and EMSCRIPTEN system environment variables
ENV EMSDK /emsdk_portable
ENV EMSCRIPTEN /emsdk_portable/links/emscripten
# But we've stored a local config in non-standard location
ENV EM_CONFIG ${EMSDK}/.emscripten
ENV EM_DATA ${EMSDK}/.data
ENV EM_CACHE ${EM_DATA}/cache
ENV EM_PORTS ${EM_DATA}/ports

# Expose standard emscripten tools like: emcc emsdk asm2wasm clang etc.. to system
ENV PATH="${EMSCRIPTEN}:${EMSDK}:${EMSDK}/links/clang/bin:${EMSDK}/links/node/bin:${EMSDK}/links/binaryen/bin:${PATH}"

# We can also use predefined entrypoint which sets up everything for us (system variables mostly)
ENTRYPOINT ["/emsdk_portable/entrypoint"]

# ------------------------------------------------------------------------------
# This section contain an arbitrary code for image customization

RUN echo "Start emscripten-ubuntu compilation" \
    &&  echo "## Create a standard user: emscripten:emscripten" \
    &&  groupadd --gid 1000 emscripten \
    &&  useradd --uid 1000 --gid emscripten --shell /bin/bash --create-home emscripten \
    \
    &&  echo "## Update and install packages" \
    &&  apt-get -qq -y update && apt-get -qq install -y --no-install-recommends \
        wget \
        git-core \
        ca-certificates \
        build-essential \
        python \
        python-pip \
        python3 \
        python3-pip \
        wget \
        curl \
        zip \
        unzip \
        git \
        ssh-client \
        ca-certificates \
        build-essential \
        make \
        cmake \
        ant \
&&  echo "\n## Done"

# ------------------------------------------------------------------------------

WORKDIR /src

# ------------------------------------------------------------------------------
# Copy used Dockerimage into image, so that it will be possible to recover any image
# Or at least inspect how it was compiled
COPY Dockerfile /emsdk_portable/dockerfiles/trzeci/emscripten-ubuntu/

LABEL maintainer="kontakt@trzeci.eu" \
      org.label-schema.name="emscripten-ubuntu" \
      org.label-schema.description="Regular version of Emscripten compiler what should be suitable to compile majority of C++ projects for Emscripten, ASM.js and WebAssembly." \
      org.label-schema.url="https://trzeci.eu" \
      org.label-schema.vcs-url="https://github.com/trzecieu/emscripten-docker" \
      org.label-schema.docker.dockerfile="/docker/trzeci/emscripten-ubuntu/Dockerfile"

# ------------------------------------------------------------------------------
