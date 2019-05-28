ARG EMSCRIPTEN_SDK=sdk-tag-1.38.25-64bit
FROM trzeci/emscripten:${EMSCRIPTEN_SDK} as emscripten_base

# ------------------------------------------------------------------------------

FROM ubuntu:bionic

COPY --from=emscripten_base /emsdk_portable /emsdk_portable

# ------------------------------------------------------------------------------

ENV EMSDK /emsdk_portable
ENV EM_DATA ${EMSDK}/.data
ENV EM_CONFIG ${EMSDK}/.emscripten
ENV EM_CACHE ${EM_DATA}/cache
ENV EM_PORTS ${EM_DATA}/ports

# ------------------------------------------------------------------------------

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

ENTRYPOINT ["/emsdk_portable/entrypoint"]
WORKDIR /src

# ------------------------------------------------------------------------------

COPY Dockerfile /emsdk_portable/dockerfiles/emscripten-ubuntu/

LABEL maintainer="kontakt@trzeci.eu" \
      org.label-schema.name="emscripten-ubuntu" \
      org.label-schema.description="Regular version of Emscripten compiler what should be suitable to compile majority of C++ projects for Emscripten, ASM.js and WebAssembly." \
      org.label-schema.url="https://trzeci.eu" \
      org.label-schema.vcs-url="https://github.com/trzecieu/emscripten-docker" \
      org.label-schema.docker.dockerfile="/docker/trzeci/emscripten-ubuntu/Dockerfile"

# ------------------------------------------------------------------------------
