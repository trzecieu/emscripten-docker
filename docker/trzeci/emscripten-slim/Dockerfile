FROM debian:jessie

# ------------------------------------------------------------------------------

ARG EMSCRIPTEN_SDK=sdk-tag-1.37.16-64bit
ARG BUILD_DATE
ARG VCS_REF

# ------------------------------------------------------------------------------

ENV EMSDK /emsdk_portable
ENV EMSCRIPTEN ${EMSDK}/sdk
ENV EM_DATA ${EMSDK}/data
ENV EM_CONFIG ${EM_DATA}/.config
ENV EM_CACHE ${EM_DATA}/.cache
ENV EM_PORTS ${EM_DATA}/.ports

# ------------------------------------------------------------------------------

LABEL maintainer="kontakt@trzeci.eu" \
      org.label-schema.name="emscripten-slim" \
      org.label-schema.description="This image includes EMSDK, Emscripten and WebAssembly compiler and tools that are very required to compile sources." \
      org.label-schema.url="https://trzeci.eu" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/asRIA/emscripten-docker" \
      org.label-schema.docker.dockerfile="/docker/trzeci/emscripten-slim/Dockerfile"

# ------------------------------------------------------------------------------

RUN echo "\n## Start building" \
    \
&&  echo "\n## Create a standard user: emscripten:emscripten" \
&&  groupadd --gid 1000 emscripten \
&&  useradd --uid 1000 --gid emscripten --shell /bin/bash --create-home emscripten \
    \
&&  echo "\n## Update and install packages" \
&&  apt-get -qq -y update && apt-get -qq install -y --no-install-recommends \
        wget \
        git-core \
        ca-certificates \
        build-essential \
        python \
        python-pip \
    \
&&  echo "\n## Installing CMake" \
&&  wget https://cmake.org/files/v3.6/cmake-3.6.3-Linux-x86_64.sh -q \
&&  mkdir /opt/cmake \
&&  printf "y\nn\n" | sh cmake-3.6.3-Linux-x86_64.sh --prefix=/opt/cmake > /dev/null \
&&  ln -s /opt/cmake/bin/cmake /usr/local/bin/cmake \
    \
&&  git clone --depth 1 https://github.com/juj/emsdk.git $EMSDK && cd $EMSDK \
&&  echo $EMSCRIPTEN_SDK | sed  's/.\+-\([0-9]\+\.[0-9]\+\.[0-9]\+\).\+/\1/g' > emscripten-tags.txt \
    \
&&  echo "\n## Compile Emscripten" \
&&  mkdir -p ${EM_DATA} \
&&  ./emsdk install node-4.1.1-64bit > /dev/null \
&&  ./emsdk install --build=MinSizeRel $EMSCRIPTEN_SDK \
    \
&&  echo "\n## Generate standard configuration" \
&&  ./emsdk activate $EMSCRIPTEN_SDK \
&&  ./emsdk construct_env > /dev/null \
&&  sed -i -e 's/4.1.1_32bit/4.1.1_64bit/g' ~/.emscripten \
    \
&&  echo "\n## Re-Configure Emscripten" \
&&  printf "import os\n"                                                >> $EM_CONFIG \
&&  printf "LLVM_ROOT='$EMSDK/llvm/clang/bin'\n"                        >> $EM_CONFIG \
&&  printf "NODE_JS='$EMSDK/node/bin/node'\n"                           >> $EM_CONFIG \
&&  printf "EMSCRIPTEN_ROOT='$EMSCRIPTEN'\n"                            >> $EM_CONFIG \
&&  printf "EMSCRIPTEN_NATIVE_OPTIMIZER='$EMSDK/optimizer/optimizer'\n" >> $EM_CONFIG \
&&  printf "SPIDERMONKEY_ENGINE=''\n"                                   >> $EM_CONFIG \
&&  printf "V8_ENGINE=''\n"                                             >> $EM_CONFIG \
&&  printf "TEMP_DIR='/tmp'\n"                                          >> $EM_CONFIG \
&&  printf "COMPILER_ENGINE=NODE_JS\n"                                  >> $EM_CONFIG \
&&  printf "JS_ENGINES=[NODE_JS]\n"                                     >> $EM_CONFIG \
&&  cat $EM_CONFIG \
    \
&&  echo "\n## Move folders according to new structure" \
&&  cat ~/.emscripten | sed -rn "s/LLVM_ROOT='(.*)'/\1/p" | xargs dirname | xargs -i mv {} {}/../clang \
&&  cat ~/.emscripten | sed -rn "s/LLVM_ROOT='(.*)'/\1/p" | xargs dirname | xargs dirname | xargs -i mv {} $EMSDK/llvm \
&&  cat ~/.emscripten | sed -rn "s/NODE_JS='(.*)'/\1/p" | xargs dirname | xargs dirname | xargs -i mv {} $EMSDK/nodejs \
&&  rm -fr $EMSDK/node \
&&  mv $EMSDK/nodejs $EMSDK/node \
&&  cat ~/.emscripten | sed -rn "s/EMSCRIPTEN_ROOT='(.*)'/\1/p" | xargs -i mv {} $EMSCRIPTEN \
&&  cat ~/.emscripten | sed -rn "s/EMSCRIPTEN_NATIVE_OPTIMIZER='(.*)'/\1/p" | xargs dirname | xargs -i mv {} $EMSDK/optimizer \
&&  rm -fr $EMSDK/emscripten \
&&  rm -fr $EMSDK/clang \
&&  rm -fr $EMSDK/emsdk_set_env.sh \
&&  rm -fr ~/.emscripten* \ 
    \
&&  echo "\n## Compile Binaryen" \
&&  $EMSCRIPTEN/embuilder.py build binaryen \
&&  mkdir $EMSDK/binaryen \
&&  mv $EM_PORTS/binaryen/binaryen-*/bin $EMSDK/binaryen/bin \
&&  printf "BINARYEN_ROOT='$EMSDK/binaryen'\n"  >> $EM_CONFIG \
    \
&&  echo "\n## Create links" \
&&  for f in $EMSDK/llvm/clang/bin $EMSDK/node/bin $EMSDK/binaryen/bin $EMSDK/optimizer $EMSDK $EMSCRIPTEN; do \
        find $f -maxdepth 1 -type f -executable | xargs -i bash -c 'ln -sf {} /usr/local/bin/$(basename {})'; \
        find $f -maxdepth 1 -type l -executable | xargs -i bash -c 'ln -sf {} /usr/local/bin/$(basename {})'; \
    done \
&&  ln -sf $EMSDK/node/bin/node /usr/local/bin/nodejs \
    \
    \
&&  echo "\n## Cleaning up Emscripten Compilation" \
&&  mv llvm/src/emscripten-version.txt emscripten-version.txt \
&&  rm -rf llvm/src \
&&  rm -rf llvm/*/lib \
&&  rm -rf llvm/*/docs \
&&  rm -rf llvm/*/tools \
&&  mkdir -p llvm/src \
&&  mv emscripten-version.txt llvm/src/emscripten-version.txt \
    \
&&  find . -name "CMakeFiles" -type d -prune -exec rm -fr {} \; \
&&  find . -name "CMakeCache.txt" -exec rm {} \; \
&&  find . -name "*.o" -exec rm {} \; \
&&  find . -name "*.a" -exec rm {} \; \
&&  find . -name "*.inc*" -exec rm {} \; \
&&  find . -name "*.gen.tmp" -exec rm {} \; \
&&  rm -fr .git bin node/*_32bit \
&&  rm -rf sdk/.git \
&&  rm -rf sdk/tests \
&&  rm -rf sdk/site \
&&  rm -rf sdk/docks \
&&  rm -rf sdk/media \
&&  rm -rf zips \
    \
&&  rm -fr /opt/cmake /usr/local/bin/cmake /cmake* \
    \
&&  echo "\n## Internal testing" \
&&  cd / \
&&  emcc --version \
&&  nodejs --version \
&&  node --version \
&&  python --version \
&&  which asm2wasm \
&&  which llvm-ar \
&&  which emsdk \
&&  which emcc \
&&  which em++ \
    \
&&  emcc --clear-cache --clear-ports \
    \
&&  echo "\n## Compile sample code" \
&&  mkdir -p /tmp/emscripten_test && cd /tmp/emscripten_test \
&&  printf '#include <iostream>\nint main(){std::cout<<"HELLO FROM DOCKER C++"<<std::endl;return 0;}' > test.cpp \
&&  em++ -O2 test.cpp -o test.js && nodejs test.js \
&&  em++ test.cpp -o test.js && nodejs test.js \
&&  em++ test.cpp -o test.js -s WASM=1 \
&&  cd / \
&&  rm -fr /tmp/emscripten_test \
    \
&&  echo "\n## Cleaning up" \
&&  find $EMSDK -name "*.pyc" -exec rm {} \; \
    \
&&  apt-get -y remove \
        build-essential \
        wget \
        ca-certificates \
        git-core \
        git \
        gcc \
        perl \
&&  apt-get -y clean \
&&  apt-get -y autoclean \
&&  apt-get -y autoremove \
    \
&&  echo "\n## Remove unused Debian files" \
&&  rm -rf /var/lib/apt/lists/* \
&&  rm -rf /var/cache/debconf/*-old \
&&  rm -rf /usr/share/doc/* \
&&  rm -rf /usr/share/man/?? \
&&  rm -rf /usr/share/man/??_* \
&&  cp -R /usr/share/locale/en\@* /tmp/ && rm -rf /usr/share/locale/* && mv /tmp/en\@* /usr/share/locale/ \
    \
&&  echo "\n## Create a mock entrypoint (compatibility)" \
&&  printf '#!/bin/bash\nexec "$@"\n' > /entrypoint \
&&  chmod 777 /entrypoint \
&&  chmod -R 777 ${EM_DATA} \
    \
&&  echo "\n## Done"

WORKDIR /src
