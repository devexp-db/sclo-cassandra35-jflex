#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: ./clean-tarball VERSION"
    exit 1
fi

VERSION=${1}
NAME="jflex"

wget http://jflex.de/${NAME}-${VERSION}.tar.gz
tar xvf ${NAME}-${VERSION}.tar.gz

(
  cd ${NAME}-${VERSION}
  find . -name "*.jar" -delete
  rm -Rf src/java_cup/ examples/
)

tar czvf ${NAME}-${VERSION}-clean.tar.gz ${NAME}-${VERSION}
rm -Rf ${NAME}-${VERSION}.tar.gz ${NAME}-${VERSION}

