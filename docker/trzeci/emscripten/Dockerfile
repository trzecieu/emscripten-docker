ARG EMSCRIPTEN_SDK=sdk-tag-1.37.16-64bit
FROM trzeci/emscripten-slim:${EMSCRIPTEN_SDK}

# ------------------------------------------------------------------------------

ARG EMSCRIPTEN_SDK

# ------------------------------------------------------------------------------

RUN echo "## Start building" \
    \
&&	echo "## Update and install packages" \
    &&	apt-get -qq -y update && apt-get -qq install -y --no-install-recommends \
        wget \
        curl \
        zip \
        unzip \
        git \
        ssh-client \
        ca-certificates \
        build-essential \
        make \
        ant \
        libidn11 \
        openjdk-8-jre-headless \
    \
&&	echo "## Installing CMake" \
    &&	wget https://cmake.org/files/v3.14/cmake-3.14.3-Linux-x86_64.sh -q \
    &&	mkdir /opt/cmake \
    &&	printf "y\nn\n" | sh cmake-3.14.3-Linux-x86_64.sh --prefix=/opt/cmake > /dev/null \
    &&		rm -fr cmake*.sh /opt/cmake/doc \
    &&		rm -fr /opt/cmake/bin/cmake-gui \
    &&		rm -fr /opt/cmake/bin/ccmake \
    &&		rm -fr /opt/cmake/bin/cpack \
    &&	ln -s /opt/cmake/bin/cmake /usr/local/bin/cmake \
    &&	ln -s /opt/cmake/bin/ctest /usr/local/bin/ctest \
    \
# activate emscripten in order to setup environment
&&  . /emsdk_portable/emsdk_set_env.sh \
&&	printf "JAVA='$(which java)'\n" >> $EM_CONFIG \
    \
&&	sleep 2 \
&&	touch ${EM_CONFIG}_sanity \
    \
&&	emcc --version \
    \
&&	emcc --clear-cache --clear-ports \
    \
&&	echo "## Compile Emscripten Ports" \
&&	${EMSCRIPTEN}/embuilder.py build ALL \
    \
    #   Manual remove cache / ports in order to keep precompiled libc/libcxx
    &&	rm -fr ${EM_CACHE}/asmjs/ports-builds \
    &&	rm -fr ${EM_PORTS} \
    \
&&	echo "## Compile sample code" \
    &&	mkdir -p /tmp/emscripten_test && cd /tmp/emscripten_test \
    &&	printf '#include <iostream>\nint main(){std::cout<<"HELLO FROM DOCKER C++"<<std::endl;return 0;}' > test.cpp \
    &&	em++ -O2 test.cpp -o test.js && node test.js \
    &&	em++ test.cpp -o test.js && node test.js \
    &&	em++ test.cpp -o test.js --closure 1 && node test.js \
        \
    &&	cd / \
    &&	rm -fr /tmp/emscripten_test \
    \
&&	echo "## Cleaning up" \
    &&	apt-mark manual make openjdk-8-jre-headless wget gcc git \
    &&	apt-get -y remove openjdk-7-jre-headless \
    &&	apt-get -y clean \
    &&	apt-get -y autoclean \
    &&	apt-get -y autoremove \
    &&	rm -rf /var/lib/apt/lists/* \
    &&	rm -rf /var/cache/debconf/*-old \
    &&	rm -rf /usr/share/doc/* \
    &&	rm -rf /usr/share/man/?? \
    &&	rm -rf /usr/share/man/??_* \
    &&	cp -R /usr/share/locale/en\@* /tmp/ && rm -rf /usr/share/locale/* && mv /tmp/en\@* /usr/share/locale/ \
    \
    &&  chmod -R 777 ${EM_DATA} \
&&	echo "## Done"

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/jre

# ------------------------------------------------------------------------------

COPY Dockerfile /emsdk_portable/dockerfiles/emscripten/

LABEL maintainer="kontakt@trzeci.eu" \
      org.label-schema.name="emscripten" \
      org.label-schema.description="Regular version of Emscripten compiler what should be suitable to compile majority of C++ projects for Emscripten, ASM.js and WebAssembly." \
      org.label-schema.url="https://trzeci.eu" \
      org.label-schema.vcs-url="https://github.com/trzecieu/emscripten-docker" \
      org.label-schema.docker.dockerfile="/docker/trzeci/emscripten/Dockerfile"

# ------------------------------------------------------------------------------