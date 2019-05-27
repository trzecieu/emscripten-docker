FROM debian:stretch AS stage_build

# ------------------------------------------------------------------------------
# -------------------------------- STAGE BUILD  --------------------------------
# ------------------------------------------------------------------------------

ARG EMSCRIPTEN_SDK=sdk-tag-1.37.16-64bit
ARG EMSDK_CHANGESET=master

# ------------------------------------------------------------------------------
# --- setup of EMSDK
ENV EMSDK=/emsdk_portable
ENV EM_DATA ${EMSDK}/.data
ENV EM_CONFIG ${EMSDK}/.emscripten
ENV EM_CACHE ${EM_DATA}/cache
ENV EM_PORTS ${EM_DATA}/ports
# ------------------------------------------------------------------------------

RUN echo "## Update and install packages" \
&&  apt-get -qq -y update && apt-get -qq install -y --no-install-recommends \
        wget \
        git-core \
        ca-certificates \
        build-essential \
        python \
        python-pip \
&&  echo "## Done"


RUN  echo "## Installing CMake" \
    &&  wget https://cmake.org/files/v3.6/cmake-3.6.3-Linux-x86_64.sh -q \
    &&  mkdir /opt/cmake \
    &&  printf "y\nn\n" | sh cmake-3.6.3-Linux-x86_64.sh --prefix=/opt/cmake > /dev/null \
    &&  ln -s /opt/cmake/bin/cmake /usr/local/bin/cmake \
&&  echo "## Done"

RUN  echo "## Get EMSDK" \
    &&  git clone https://github.com/juj/emsdk.git ${EMSDK} && cd ${EMSDK} && git reset --hard ${EMSDK_CHANGESET} \
        \
    # Update emscripten-tags.txt file manually with request version
    &&  echo ${EMSCRIPTEN_SDK} | sed  's/.\+-\([0-9]\+\.[0-9]\+\.[0-9]\+\).\+/\1/g' > emscripten-tags.txt \
&&  echo "## Done"

RUN echo "## Compile Emscripten" \
    &&  cd ${EMSDK} \
        \
    &&  ./emsdk install node-8.9.1-64bit > /dev/null \
    # Compile llvm with dynamic libs support (size optimization)
    &&  LLVM_CMAKE_ARGS=-DLLVM_LINK_LLVM_DYLIB=ON,-DLLVM_LINK_LLVM_DYLIB=ON \
        ./emsdk install --build=MinSizeRel ${EMSCRIPTEN_SDK} \
        \
&&  echo "## Done"

# this generates configuration that contains all valid paths
RUN cd ${EMSDK} \
    &&  echo "## Generate standard configuration" \
    &&  ./emsdk activate ${EMSCRIPTEN_SDK} --embedded \
    &&  ./emsdk construct_env > /dev/null \
        \
    # remove wrongly created entry with EM_CACHE, variable will be picked up from ENV
    &&  sed -i -e "/EM_CACHE/d" ${EMSDK}/emsdk_set_env.sh \
        \
&&  echo "## Done"

# create structure and make mutable folders accessible for r/w
RUN cd ${EMSDK} \
    &&  echo "## Create .data structure" \
    &&  for mutable_dir in ${EM_DATA} ${EM_PORTS} ${EM_CACHE} ${EMSDK}/zips ${EMSDK}/tmp; do \
            mkdir -p ${mutable_dir}; \
            chmod -R 777 ${mutable_dir}; \
        done \
        \
&&  echo "## Done"

# RUN cd ${EMSDK} \
#     &&  echo "## Create SDK symlink" \
#     &&  . ./emsdk_set_env.sh \
#     &&  ln -s $(dirname $(which emcc)) ${EMSDK}/sdk \
# &&  echo "## Done"

# Building uses some bashizm
SHELL ["/bin/bash", "-c"]
RUN cd ${EMSDK} \
    &&  echo "## Clean-up Emscripten Installation" \
    # Allow to use ** for recursive wildcard - bash only!
    &&  shopt -s globstar \
        \
    # Issue #34: emcc.txt file is essencial for error free execution of emcc
    &&  _file=`echo ./emscripten/*/site/build/text/docs/tools_reference/emcc.txt` \
    &&  _content=`cat ${_file}` \
    &&  rm -fr \
            ./emscripten/*/docs \
            ./emscripten/*/media \
            ./emscripten/*/site \
    &&  mkdir -p `dirname ${_file}` \
    &&  echo ${_content} >> ${_file} \
        \
    # emscripten-version.txt is crucial to make emcc work
    &&  _file=`echo clang/*/src/emscripten-version.txt` \
    &&  _content=`cat ${_file}` \
    &&  rm -fr clang/*/src \
    &&  mkdir -p `dirname ${_file}` \
    &&  echo ${_content} >> ${_file} \
    \
    # will clean both: bin and src folder
    &&  rm -fr binaryen/*/src \
    &&  rm -fr binaryen/**/test \
    &&  rm -fr binaryen/**/*.cmake \
    &&  rm -fr binaryen/**/Makefile \
    \
    &&  rm -fr clang/*/*/docs \
    &&  rm -fr clang/*/*/tools \
    &&  rm -fr clang/*/*/projects \
    &&  rm -fr clang/*/*/cmake \
    &&  rm -fr clang/**/*.cmake \
    &&  rm -fr clang/**/Makefile \
        \
    &&  find . -name "*.pyc" -exec rm {} \; \
    &&  find . -name "CMakeFiles" -type d -prune -exec rm -fr {} \; \
    &&  find . -name "CMakeCache.txt" -exec rm {} \; \
        \
    &&  find . -name "*.o" -exec rm {} \; \
    &&  find . -name "*.a" -exec rm {} \; \
    &&  find . -name "*.inc*" -exec rm {} \; \
    &&  find . -name "*.gen.tmp" -exec rm {} \; \
        \
    # remove empty folders
    &&  find clang -type d -depth -empty -exec rmdir "{}" \; \
    &&  find binaryen -type d -depth -empty -exec rmdir "{}" \; \
        \
    &&  rm -fr **/*_32bit \
    &&  rm -rf **/.git \
    &&  rm -rf **/tests \
    &&  rm -fr zips/* \
        \
    &&  rm -fr /opt/cmake /usr/local/bin/cmake /cmake* \
        \
    # sleep will make sure that created cache will be stored correctly
    &&  sleep 2 \
&&  echo "## Done"

# ------------------------------------------------------------------------------
ENV EMSDK_ENTRYPOINT=${EMSDK}/entrypoint

# compatibility user with an old solution that bases on custom user
RUN echo "## Create transferable entrypoint" \
    &&  printf '#!/bin/bash\n'                                          >  ${EMSDK_ENTRYPOINT} \
    # In case when mapped user id with `docker run -u` is not created ($HOME is '/')
    # then we map HOME to /tmp as it should r/w for everyone
    &&  printf 'if [ "$HOME" = "/" ] ; then\n'                          >> ${EMSDK_ENTRYPOINT} \
    &&  printf '    export HOME=/tmp\n'                                 >> ${EMSDK_ENTRYPOINT} \
    &&  printf 'fi\n'                                                   >> ${EMSDK_ENTRYPOINT} \
    &&  printf '\n'                                                     >> ${EMSDK_ENTRYPOINT} \
    # In case of running as root, uses umask to reduce problem of file permission on host
    &&  printf 'if [ "$(id -g)" = "0" ] && [ "$(id -u)" = "0" ] ;\n'    >> ${EMSDK_ENTRYPOINT} \
    &&  printf 'then\n'                                                 >> ${EMSDK_ENTRYPOINT} \
    &&  printf '    umask 0000\n'                                       >> ${EMSDK_ENTRYPOINT} \
    &&  printf 'fi\n'                                                   >> ${EMSDK_ENTRYPOINT} \
    # export this image specific Environment variables
    &&  printf "export EMSDK=${EMSDK}\n"                                >> ${EMSDK_ENTRYPOINT} \
    # &&  printf "export EMSCRIPTEN=${EMSCRIPTEN}\n"                      >> ${EMSDK_ENTRYPOINT} \
    &&  printf "export EM_DATA=${EM_DATA}\n"                            >> ${EMSDK_ENTRYPOINT} \
    &&  printf "export EM_CONFIG=${EM_CONFIG}\n"                        >> ${EMSDK_ENTRYPOINT} \
    &&  printf "export EM_CACHE=${EM_CACHE}\n"                          >> ${EMSDK_ENTRYPOINT} \
    &&  printf "export EM_PORTS=${EM_PORTS}\n"                          >> ${EMSDK_ENTRYPOINT} \
    # activate emscripten before executions
    &&  printf '. ${EMSDK}/emsdk_set_env.sh > /dev/null\n'              >> ${EMSDK_ENTRYPOINT} \
    # Forward command
    &&  printf '"$@"\n'                                                 >> ${EMSDK_ENTRYPOINT} \
    \
    &&  chmod +x ${EMSDK_ENTRYPOINT} \
    \
&&  echo "## Done"


# populate cache for libc++, to improve further compilations
RUN echo "## Pre-populate cache" \
    &&  . ${EMSDK}/emsdk_set_env.sh \
    \
    &&  mkdir -p /tmp/emscripten_test &&  cd /tmp/emscripten_test \
    \
    &&  printf '#include <iostream>\nint main(){std::cout << "HELLO FROM DOCKER C++"<<std::endl;return 0;}' > test.cpp \
    &&  em++ --std=c++11 test.cpp -o test.js -s WASM=0 &&  node test.js \
    &&  em++ --std=c++11 -g4 test.cpp -o test.js -s WASM=0 &&  node test.js \
    &&  em++ --std=c++11 test.cpp -o test.js -s WASM=1 &&  node test.js \
    &&  cd / \
    &&  rm -fr /tmp/emscripten_test \
    \
    # some files were created, and we need to make sure that those can be accessed by non-root people
    &&  chmod -R 777 ${EM_DATA} \
    \
    # cleanup
    &&  find ${EMSDK} -name "*.pyc" -exec rm {} \; \
    \
    &&  echo "## Done"

# ------------------------------------------------------------------------------
# -------------------------------- STAGE DEPLOY --------------------------------
# ------------------------------------------------------------------------------

FROM debian:stretch AS stage_deploy

# unfrtunately ENVs and ARGs aren't forwareded to substage :< :<
COPY --from=stage_build /emsdk_portable /emsdk_portable

# Export some variables (compatibility reason)
ENV EMSDK=/emsdk_portable
ENV EM_DATA ${EMSDK}/.data
ENV EM_CONFIG ${EMSDK}/.emscripten
ENV EM_CACHE ${EM_DATA}/cache
ENV EM_PORTS ${EM_DATA}/ports

# ------------------------------------------------------------------------------

# Create a 'standard` 1000:1000 user, mostly compatibility reasons
RUN echo "## Create entrypoint" \
    &&  groupadd --gid 1000 emscripten \
    &&  useradd --uid 1000 --gid emscripten --shell /bin/bash --create-home emscripten \
    \
&&  echo "## Done"


RUN echo "## Update and install packages" \
&&  apt-get -qq -y update && apt-get -qq install -y --no-install-recommends \
        ca-certificates \
        python \
        python-pip \
    \
    # Standard Cleanup on Debian images
    &&  apt-get -y clean \
    &&  apt-get -y autoclean \
    &&  apt-get -y autoremove \
    &&  rm -rf /var/lib/apt/lists/* \
    &&  rm -rf /var/cache/debconf/*-old \
    &&  rm -rf /usr/share/doc/* \
    &&  rm -rf /usr/share/man/?? \
    &&  rm -rf /usr/share/man/??_* \
&&  echo "## Done"

# Docker's convention is to create entrypoint in /entrypoint path.
# Let's create this entrypoint for compatybility and to keep tradition
RUN echo "## Create standard docker entrypoint" \
    &&  printf '#!/bin/bash\n'                  >  /entrypoint \
    &&  printf ". ${EMSDK}/entrypoint \"$@\"\n"     >> /entrypoint \
    \
    &&  chmod +x /entrypoint \
    \
&&  echo "## Done"

ENTRYPOINT ["/emsdk_portable/entrypoint"]
WORKDIR /src

# ------------------------------------------------------------------------------
COPY ./Dockerfile /dockerfiles/emscripten-slim/

LABEL maintainer="kontakt@trzeci.eu" \
      org.label-schema.name="emscripten-slim" \
      org.label-schema.description="This image includes EMSDK, Emscripten and WebAssembly compiler and tools that are very required to compile sources." \
      org.label-schema.url="https://trzeci.eu" \
      org.label-schema.vcs-url="https://github.com/trzecieu/emscripten-docker" \
      org.label-schema.docker.dockerfile="/docker/trzeci/emscripten-slim/Dockerfile"

# ------------------------- POST BUILD IN-PLACE TESTING ------------------------

RUN echo "## Internal Testing of image " \
    &&  . ${EMSDK}/emsdk_set_env.sh \
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
