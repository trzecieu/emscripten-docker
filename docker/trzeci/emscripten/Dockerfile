ARG EMSCRIPTEN_SDK=sdk-tag-1.37.16-64bit
FROM trzeci/emscripten-slim:${EMSCRIPTEN_SDK}

# ------------------------------------------------------------------------------

ARG VCS_REF
ARG BUILD_DATE
ARG EMSCRIPTEN_SDK

# ------------------------------------------------------------------------------

LABEL maintainer="kontakt@trzeci.eu" \
      org.label-schema.name="emscripten" \
      org.label-schema.description="Regular version of Emscripten compiler what should be suitable to compile majority of C++ projects for Emscripten, ASM.js and WebAssembly." \
      org.label-schema.url="https://trzeci.eu" \
      org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="https://github.com/asRIA/emscripten-docker" \
      org.label-schema.docker.dockerfile="/docker/trzeci/emscripten/Dockerfile"

# ------------------------------------------------------------------------------

RUN echo "\n## Start building" \
    \
&&	echo "\n## Update and install packages" \
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
        openjdk-7-jre-headless \
        libidn11 \
    \
&&	echo "\n## Installing CMake" \
&&	wget https://cmake.org/files/v3.6/cmake-3.6.3-Linux-x86_64.sh -q \
&&	mkdir /opt/cmake \
&&	printf "y\nn\n" | sh cmake-3.6.3-Linux-x86_64.sh --prefix=/opt/cmake > /dev/null \
&&		rm -fr cmake*.sh /opt/cmake/doc \
&&		rm -fr /opt/cmake/bin/cmake-gui \
&&		rm -fr /opt/cmake/bin/ccmake \
&&		rm -fr /opt/cmake/bin/cpack \
&&	ln -s /opt/cmake/bin/cmake /usr/local/bin/cmake \
&&	ln -s /opt/cmake/bin/ctest /usr/local/bin/ctest \
    \
&&	printf "JAVA='$(which java)'\n" >> $EM_CONFIG \
    \
&&	sleep 2 \
&&	touch ${EM_CONFIG}_sanity \
    \
&&	emcc --version \
    \
&&	emcc --clear-cache --clear-ports \
    \
&&	echo "\n## Compile Emscripten Ports" \
&&	$EMSCRIPTEN/embuilder.py build ALL \
&&	rm -fr $EM_CACHE/asmjs/ports-builds \
&&	rm -fr $EM_PORTS \
    \
&&	echo "\n## Compile sample code" \
&&	mkdir -p /tmp/emscripten_test && cd /tmp/emscripten_test \
&&	printf '#include <iostream>\nint main(){std::cout<<"HELLO FROM DOCKER C++"<<std::endl;return 0;}' > test.cpp \
&&	em++ -O2 test.cpp -o test.js && nodejs test.js \
&&	em++ test.cpp -o test.js && nodejs test.js \
&&	em++ test.cpp -o test.js --closure 1 && nodejs test.js \
    \
&&	cd / \
&&	rm -fr /tmp/emscripten_test \
    \
&&	echo "\n## Cleaning up" \
&&	apt-mark manual make openjdk-7-jre-headless wget gcc git \
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
&&	echo "\n## Installed packages:" \
&&	apt-mark showmanual | xargs -I % sh -c 'echo "  * \`%\` : **"$(xargs dpkg -s % | grep Version | sed  "s/Version: //")"**"' \
    \
&&  chmod -R 777 ${EM_DATA} \
&&	echo "\n## Done"

ENV JAVA_HOME /usr/lib/jvm/java-7-openjdk-amd64/jre
