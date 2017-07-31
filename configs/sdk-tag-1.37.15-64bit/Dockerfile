FROM debian:jessie
MAINTAINER kontakt@trzeci.eu

RUN rm /bin/sh && ln -s /bin/bash /bin/sh \
&&	apt-get -y update && apt-get install -y --no-install-recommends \
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
&&	git clone --depth 1 https://github.com/juj/emsdk.git emsdk_portable \
&&	cd emsdk_portable \
&&	rm -fr .git \
&&	rm -fr bin \
&&	echo 1.37.15 > emscripten-tags.txt \
	\
&&	echo "## Compile Emscripten" \
&&	./emsdk install --build=MinSizeRel sdk-tag-1.37.15-64bit \
&&	./emsdk activate sdk-tag-1.37.15-64bit \
	\
&&	rm -rf node \
&&	./emsdk install node-4.1.1-64bit \
&&	ln -sf /emsdk_portable/node/4.1.1_64bit/bin/node /usr/local/bin/nodejs \
&&	ln -sf /emsdk_portable/node/4.1.1_64bit/bin/node /usr/local/bin/node \
&&	ln -sf /emsdk_portable/node/4.1.1_64bit/bin/npm /usr/local/bin/npm \
&&	sed -i -e 's/NODE_JS=.*/NODE_JS="nodejs"/g' ~/.emscripten \
&&	printf "JAVA = '$(which java)'\n" >> ~/.emscripten \
	\
&&	echo "## Cleaning up" \
&&	find . -name "CMakeFiles" -type d -prune -exec rm -fr {} \; \
&&	find . -name "*.o" -exec rm {} \; \
&&	find . -name "*.a" -exec rm {} \; \
&&	emscripten_version=$(find clang/*/src/emscripten-version.txt) \
&&	mv $emscripten_version emscripten-version.txt \
&&	rm -rf clang/*/src \ 
&&	mkdir -p $(echo "$(dirname "$emscripten_version")") \ 
&&	mv emscripten-version.txt $emscripten_version \
&&	rm -rf emscripten/*/.git \
&&	rm -rf zips \
&&	rm -rf emscripten/*/tests \
	\
&&	for prog in em++ em-config emar emcc emconfigure emmake emranlib emrun emscons emcmake; do \
	ln -sf /emsdk_portable/emscripten/tag-1.37.15/$prog /usr/local/bin; done \
&&	ln -sf /emsdk_portable/emsdk /usr/local/bin/emsdk \
	\
&&	EMSCRIPTEN=/emsdk_portable/emscripten/tag-1.37.15 \
	\
&&	emcc --version \
	\
&&	echo "## Compile sample code" \
&&	mkdir -p /tmp/emscripten_test && cd /tmp/emscripten_test \
&&	printf '#include <iostream>\nint main(){std::cout<<"HELLO"<<std::endl;return 0;}' > test.cpp \
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
&&	echo "## Done"

# SETUP SDK
ENV EMSCRIPTEN=/emsdk_portable/emscripten/tag-1.37.15
ENV JAVA_HOME /usr/lib/jvm/java-7-openjdk-amd64/jre

WORKDIR /src
