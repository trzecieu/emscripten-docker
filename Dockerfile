FROM debian:jessie
MAINTAINER kontakt@trzeci.eu

# dynamically injected by ./build script
ARG EMSCRIPTEN_SDK=sdk-tag-1.37.16-64bit
# TODO: Deduce following
ARG EMSCRIPTEN_SDK_DIR=tag-1.37.16
ARG EMSCRIPTEN_TAG=1.37.16

# hardcoded
ARG EMSDK=/emsdk_portable

ADD	entrypoint /
RUN echo "## Start building" \
	\
&&	chmod 777 /entrypoint
	\
&&	echo "## Update and install packages" \
&&	apt-get -q -y update && apt-get -q install -y --no-install-recommends \
	wget git-core ca-certificates build-essential python libidn11 openjdk-7-jre-headless \
	\
&&	echo "## Installing CMAKE" \
&&	wget https://cmake.org/files/v3.6/cmake-3.6.3-Linux-x86_64.sh -q \
&&	mkdir /opt/cmake \
&&	printf "y\nn\n" | sh cmake-3.6.3-Linux-x86_64.sh --prefix=/opt/cmake \
&&		rm -fr cmake*.sh /opt/cmake/doc \
&&		rm -fr /opt/cmake/bin/cmake-gui \
&&		rm -fr /opt/cmake/bin/ccmake \
&&		rm -fr /opt/cmake/bin/cpack \
&&	ln -s /opt/cmake/bin/cmake /usr/local/bin/cmake \
	\
&&	git clone --depth 1 https://github.com/juj/emsdk.git $EMSDK \
&&	cd $EMSDK \
&&	rm -fr .git \
&&	rm -fr bin \
&&	echo $EMSCRIPTEN_TAG > emscripten-tags.txt \
	\
&&	echo "## Compile Emscripten" \
&&	./emsdk install --build=MinSizeRel $EMSCRIPTEN_SDK \
&&	./emsdk activate $EMSCRIPTEN_SDK \
	\
&&	rm -rf node \
&&	./emsdk install node-4.1.1-64bit \
&&	ln -sf $EMSDK/node/4.1.1_64bit/bin/node /usr/local/bin/nodejs \
&&	ln -sf $EMSDK/node/4.1.1_64bit/bin/node /usr/local/bin/node \
&&	ln -sf $EMSDK/node/4.1.1_64bit/bin/npm /usr/local/bin/npm \
&&	sed -i -e 's/NODE_JS=.*/NODE_JS="nodejs"/g' ~/.emscripten \
&&	printf "JAVA = '$(which java)'\n" >> ~/.emscripten \
	\
&&	echo "## Cleaning up" \
&&	find . -name "CMakeFiles" -type d -prune -exec rm -fr {} \; \
&&	find . -name "*.o" -exec rm {} \; \
&&	find . -name "*.a" -exec rm {} \; \
	\
&&	emscripten_version_file=$(find clang/*/src/emscripten-version.txt) \
&&	mv $emscripten_version_file emscripten-version.txt \
&&	rm -rf clang/*/src \ 
&&	mkdir -p $(echo "$(dirname "$emscripten_version_file")") \ 
&&	mv emscripten-version.txt $emscripten_version_file \
	\
&&	rm -rf emscripten/*/.git \
&&	rm -rf zips \
&&	rm -rf emscripten/*/tests \
	\
&&	for prog in em++ em-config emar emcc emconfigure emmake emranlib emrun emscons emcmake; do \
	ln -sf $EMSDK/emscripten/$EMSCRIPTEN_SDK_DIR/$prog /usr/local/bin; done \
&&	ln -sf $EMSDK/emsdk /usr/local/bin/emsdk \
	\
&&	EMSCRIPTEN=$EMSDK/emscripten/$EMSCRIPTEN_SDK_DIR \
	\
&&	emcc --version \
	\
&&	echo "## Compile sample code" \
&&	mkdir -p /tmp/emscripten_test && cd /tmp/emscripten_test \
&&	printf '#include <iostream>\nint main()$std::cout<<"HELLO FROM DOCKER C++"<<std::endl;return 0;' > test.cpp \
&&	em++ -O2 test.cpp -o test.js && nodejs test.js \
&&	em++ test.cpp -o test.js && nodejs test.js \
&&	em++ test.cpp -o test.js --closure 1 && nodejs test.js \
	\
&&	echo "## Compile Emscripten Ports" \
&&	emcc --clear-cache --clear-ports \
&&	$EMSCRIPTEN/embuilder.py build ALL \
&&	rm -fr ~/.emscripten_cache/asmjs/ports-builds \
&&	rm -fr ~/.emscripten_ports \
	\
&&	cd / \
&&	rm -fr /tmp/emscripten_test \
	\
&&	echo "## Cleaning up" \
&&	apt-mark manual make openjdk-7-jre-headless \
&&	apt-get -y remove \
	gcc perl git-core wget build-essential git \
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
&&	echo "## Done"

# SETUP SDK
ENV JAVA_HOME /usr/lib/jvm/java-7-openjdk-amd64/jre

WORKDIR /src

CMD ["/bin/bash"]
ENTRYPOINT ["/entrypoint"]
