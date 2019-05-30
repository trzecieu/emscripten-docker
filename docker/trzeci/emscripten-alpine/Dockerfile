ARG EMSCRIPTEN_SDK=sdk-tag-1.38.25-64bit
FROM trzeci/emscripten-slim:${EMSCRIPTEN_SDK} as emscripten_base

# ------------------------------------------------------------------------------

FROM alpine

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
# Copy used Dockerimage into image, so that it will be possible to recover any image
# Or at least inspect how it was compiled
COPY Dockerfile /emsdk_portable/dockerfiles/trzeci/emscripten-alpine/

LABEL maintainer="kontakt@trzeci.eu" \
      org.label-schema.name="emscripten-alpine" \
      org.label-schema.description="Regular version of Emscripten compiler what should be suitable to compile majority of C++ projects for Emscripten, ASM.js and WebAssembly." \
      org.label-schema.url="https://trzeci.eu" \
      org.label-schema.vcs-url="https://github.com/trzecieu/emscripten-docker" \
      org.label-schema.docker.dockerfile="/docker/trzeci/emscripten-alpine/Dockerfile"

# ------------------------------------------------------------------------------
