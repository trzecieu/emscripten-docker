FROM debian:jessie
ARG EMSCRIPTEN_SDK=sdk-tag-1.37.16-64bit

ARG BUILD_DATE
ARG VCS_REF

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
&&  EMSDK=/emsdk_portable \
    \
&&	echo "\n## Update and install packages" \
&&	apt-get -qq -y update && apt-get -qq install -y --no-install-recommends \
        wget \
        git-core \
        ca-certificates \
        build-essential \
        python \
    \
&&	echo "\n## Installing CMAKE" \
&&	wget https://cmake.org/files/v3.6/cmake-3.6.3-Linux-x86_64.sh -q \
&&	mkdir /opt/cmake \
&&	printf "y\nn\n" | sh cmake-3.6.3-Linux-x86_64.sh --prefix=/opt/cmake > /dev/null \
&&		rm -fr cmake*.sh /opt/cmake/doc \
&&		rm -fr /opt/cmake/bin/cmake-gui \
&&		rm -fr /opt/cmake/bin/ccmake \
&&		rm -fr /opt/cmake/bin/cpack \
&&	ln -s /opt/cmake/bin/cmake /usr/local/bin/cmake \
    \
&&	git clone --depth 1 https://github.com/juj/emsdk.git $EMSDK && cd $EMSDK \
&&	echo $EMSCRIPTEN_SDK | sed  's/.\+-\([0-9]\+\.[0-9]\+\.[0-9]\+\).\+/\1/g' > emscripten-tags.txt \
    \
&&	echo "\n## Compile Emscripten" \
&&	./emsdk install node-4.1.1-64bit \
&&	ln -sf $EMSDK/node/4.1.1_64bit/bin/node $EMSDK/node/4.1.1_64bit/bin/nodejs \
    \
&&	./emsdk install --build=MinSizeRel $EMSCRIPTEN_SDK \
    \
&&	echo "\n## Configure Emscripten" \
&&  ./emsdk activate $EMSCRIPTEN_SDK \
&&	./emsdk construct_env > /dev/null \
&&	sed -i -e 's/4.1.1_32bit/4.1.1_64bit/g' ~/.emscripten \
&&	sed -i -e 's/4.1.1_32bit/4.1.1_64bit/g' ./emsdk_set_env.sh \
    \
&&  . ./emsdk_set_env.sh \
    \
&&	emscripten_version_file=$(find clang/*/src/emscripten-version.txt) \
&&	mv $emscripten_version_file emscripten-version.txt \
&&	rm -rf clang/*/src \ 
&&	mkdir -p $(echo "$(dirname "$emscripten_version_file")") \ 
&&	mv emscripten-version.txt $emscripten_version_file \
    \
&&	echo "\n## Cleaning up Emscripten Compilation" \
&&	find . -name "CMakeFiles" -type d -prune -exec rm -fr {} \; \
&&	find . -name "*.o" -exec rm {} \; \
&&	find . -name "*.a" -exec rm {} \; \
&&	find . -name "*.inc*" -exec rm {} \; \
&&	rm -fr .git bin node/*_32bit \
&&	rm -rf emscripten/*/.git \
&&	rm -rf emscripten/*/tests \
&&	rm -rf zips \
    \
&&	rm -fr /opt/cmake /usr/local/bin/cmake \
    \
&&	emcc --version \
&&	emcc --clear-cache --clear-ports \
    \
&&	echo "\n## Compile sample code" \
&&	mkdir -p /tmp/emscripten_test && cd /tmp/emscripten_test \
&&	printf '#include <iostream>\nint main(){std::cout<<"HELLO FROM DOCKER C++"<<std::endl;return 0;}' > test.cpp \
&&	em++ -O2 test.cpp -o test.js && nodejs test.js \
&&	em++ test.cpp -o test.js && nodejs test.js \
&&	cd / \
&&	rm -fr /tmp/emscripten_test \
    \
&&	echo "\n## Cleaning up" \
&&  cd $EMSDK \
&&	find . -name "*.pyc" -exec rm {} \; \
&&  cd / \
    \
&&	apt-get -y remove \
        build-essential \
        wget \
        ca-certificates \
        git-core \
        git \
        gcc \
        perl \
&&	apt-get -y clean \
&&	apt-get -y autoclean \
&&	apt-get -y autoremove \
    \
&&	rm -rf /var/lib/apt/lists/* \
&&	rm -rf /var/cache/debconf/*-old \
&&	rm -rf /usr/share/doc/* \
&&	rm -rf /usr/share/man/?? \
&&	rm -rf /usr/share/man/??_* \
&&	cp -R /usr/share/locale/en\@* /tmp/ && rm -rf /usr/share/locale/* && mv /tmp/en\@* /usr/share/locale/ \
    \
&&	echo "\n## Create entrypoint" \
&&  printf '#!/bin/bash\n'                                      >> /entrypoint \
&&  printf 'set -e\n'                                           >> /entrypoint \
&&  printf ". $EMSDK/emsdk_set_env.sh ?> /dev/null\n"           >> /entrypoint \
&&  printf 'exec "$@"\n'                                        >> /entrypoint \
&&	chmod 777 /entrypoint \
    \
&&	echo "\n## Done"

WORKDIR /src

CMD ["/bin/bash"]
ENTRYPOINT ["/entrypoint"]
