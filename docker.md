### Structure
Each tag was build from generated Dockerfile. Source of generator and template you can find in [GitHub repo](https://github.com/asRIA/emscripten-docker/tree/master/configs).
* Base system: **Debian Jessie**
* Installed packages: 
  * `cmake`: 3.6.3
  * `make`: 4.0
  * `python`: 2.7
  * `nodejs`: 4.1 (from EMSDK)
  * `java`: OpenJDK 1.7.0_131
* Version of Emscripten:  **32bit** and **64bit**
* Starting from **1.36.7** images are bundled with cmake 3.6.3


debian:jessie has been chosen in order to have the latest ImageMagick. It is not a part of this image but this image could be easy extend to pull it. Image has been optimised in order to have the lowest possible size.

#### History
* from **1.37.10** images are bundled with `java`
* from **1.36.7** images are bundled with `make` and `nodejs`
* from **1.36.7** images are bundled with `cmake` 3.6.3
* from **1.35.0** images based on Debian
* from **1.34.X** images based on Ubuntu:15.10

### Tag schema
#### latest
Currently latest tag is not available. Not decided yet it should point either on the latest master, or latest official release. 

#### Version release
`sdk-tag-{VERSION}-{BITS}`
where
**VERSION**: One of the official version released since 1.34.1
**BITS**: `["32bit", "64bit"]`
Example: `sdk-tag-1.34.4-64bit`

#### Branch release
`sdk-{BRANCH}-{BITS}`
where
**BRANCH**: `["incoming", "master"]`
**BITS**: `["32bit", "64bit"]`
Example: `sdk-master-32bit`

### How to use?
Start volume should be mounted in `/src`. 
For start point every Emscripten command is available. For the instance: emcc, em++, emmake, emar etc.

To compile single file it could be called like:
`docker run -v $(pwd):/src trzeci/emscripten:sdk-tag-1.35.4-64bit emcc helloworld.cpp -o helloworld.js`

This container nicely works with cmake projects

### GitHub / Issue tracker
https://github.com/asRIA/emscripten-docker