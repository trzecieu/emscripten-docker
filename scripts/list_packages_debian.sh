#!/bin/bash
apt-mark showmanual | xargs -I % sh -c "echo %:\$(xargs dpkg -s % | grep Version | sed  \"s/Version: //\")"