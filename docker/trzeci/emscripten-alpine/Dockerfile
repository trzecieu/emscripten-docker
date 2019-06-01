ARG EMSCRIPTEN_SDK=sdk-tag-1.38.25-64bit
FROM trzeci/emscripten-slim:${EMSCRIPTEN_SDK} as emscripten_base

# ------------------------------------------------------------------------------
# Entries in this section is required to move Emscripten SDK to another base image

# Any arbitrary base image of choice
FROM alpine

# Source /emsdk_portable contains every emscripten tool.
# It's not recommended to change destination path
COPY --from=emscripten_base /emsdk_portable /emsdk_portable


# Fallback in case Emscripten isn't activated.
# This will let use tools offered by this image inside other Docker images (sub-stages) or with custom / no entrypoint
ENV EMSDK /emsdk_portable
ENV EMSCRIPTEN=${EMSDK}/emscripten/sdk
ENV EM_DATA ${EMSDK}/.data
ENV EM_CONFIG ${EMSDK}/.emscripten
ENV EM_CACHE ${EM_DATA}/cache
ENV EM_PORTS ${EM_DATA}/ports

# Fallback in case Emscripten isn't activated
# Expose Major tools to system PATH, so that emcc, node, asm2wasm etc can be used without activation
ENV PATH="${EMSCRIPTEN}:${EMSDK}:${EMSDK}/llvm/clang/bin:${EMSDK}/node/current/bin:${EMSDK}/binaryen/bin:${PATH}"

# Use entrypoint that's coming from emscripten-slim image. It sets all required system paths and variables
ENTRYPOINT ["/emsdk_portable/entrypoint"]

# ------------------------------------------------------------------------------

RUN echo "## Start emscripten-ubuntu compilation" \
    &&  echo "## Create a standard user: emscripten:emscripten" \
    &&  addgroup -S emscripten && adduser -S emscripten -G emscripten \
    \
    &&  echo "## Update and install packages" \
    &&  apk add --update \
        nodejs \
        bash \
        python \
        py-pip \
        make \
        ca-certificates \
&&  echo "## Done"

RUN echo "## Internal Testing of image " \
    &&  . /emsdk_portable/emsdk_set_env.sh \
    &&  set -x \
    &&  which asm2wasm \
    &&  which llvm-ar \
    &&  which emsdk \
    &&  node --version \
    &&  npm --version \
    &&  python --version \
    &&  pip --version \
    \
    &&  em++ --version \
    &&  emcc --version \
    \
    &&  find ${EMSDK} -name "*.pyc" -exec rm {} \; \
    \
&&  echo "## Done"

# ------------------------------------------------------------------------------

WORKDIR /src

# ------------------------------------------------------------------------------
# Copy this Dockerimage into image, so that it will be possible to recreate it later
COPY Dockerfile /emsdk_portable/dockerfiles/trzeci/emscripten-alpine/

LABEL maintainer="kontakt@trzeci.eu" \
      org.label-schema.name="emscripten-alpine" \
      org.label-schema.description="Regular version of Emscripten compiler what should be suitable to compile majority of C++ projects for Emscripten, ASM.js and WebAssembly." \
      org.label-schema.url="https://trzeci.eu" \
      org.label-schema.vcs-url="https://github.com/trzecieu/emscripten-docker" \
      org.label-schema.docker.dockerfile="/docker/trzeci/emscripten-alpine/Dockerfile"

# ------------------------------------------------------------------------------
