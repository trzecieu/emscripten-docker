ARG EMSCRIPTEN_SDK=sdk-tag-1.38.25-64bit
FROM trzeci/emscripten-slim:${EMSCRIPTEN_SDK} as emscripten_base

# ------------------------------------------------------------------------------

FROM alpine

COPY --from=emscripten_base /emsdk_portable /emsdk_portable

# ------------------------------------------------------------------------------

RUN echo "Start emscripten-ubuntu compilation" \
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
&&  echo "\n## Done"

RUN echo "## Internal Testing of image " \
# TODO: Investigate missing EMSDK_CONFIG export here
    &&  . /emsdk_portable/entrypoint \
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

ENTRYPOINT ["/emsdk_portable/entrypoint"]
WORKDIR /src

# ------------------------------------------------------------------------------

COPY ./Dockerfile /dockerfiles/emscripten-alpine/

LABEL maintainer="kontakt@trzeci.eu" \
      org.label-schema.name="emscripten-alpine" \
      org.label-schema.description="Regular version of Emscripten compiler what should be suitable to compile majority of C++ projects for Emscripten, ASM.js and WebAssembly." \
      org.label-schema.url="https://trzeci.eu" \
      org.label-schema.vcs-url="https://github.com/trzecieu/emscripten-docker" \
      org.label-schema.docker.dockerfile="/docker/trzeci/emscripten-alpine/Dockerfile"

# ------------------------------------------------------------------------------
