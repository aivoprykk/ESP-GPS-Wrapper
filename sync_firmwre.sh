#!/bin/bash
version=
host=10.10.19.80
dir=/srv/samba/esplogger/firmware/versions
src=".pio/build/release/firmware_v_*.bin"
if [ "$1" != "" ]; then version=$1; fi
if [ "$HOST" != "" ]; then host=$HOST; fi
if [ -z "$version" ]; then version=$(echo $src|perl -ne 's!.*firmware_v_([\d]+)\.bin!$1!; print'); fi
rsync -av $src root@$host:$dir/$version/ && echo $version|ssh root@$host "tee $dir/_latest"