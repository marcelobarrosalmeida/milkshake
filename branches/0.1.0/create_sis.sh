#!/bin/bash
#
# DO NOT TRY TO GENERATE THE SIS FILE IF YOUR PATH CONTAINS SPACES.
# ENSYMBLE DOES NOT SUPPORT THEM ! COPY THIS PROJECT TO C:\
# BEFORE RUNNING THIS SCRIPT.
#

if [ -z "$1" ]; then
    echo "Sintaxe: $0 VERSION"
    exit 1
fi

PYTHON=python2.5
APPNAME=Milkshake
CAPBLS=NetworkServices+LocalServices+ReadUserData+WriteUserData+UserEnvironment
SRCDIR=src
TMPDIR=src.tmp
ICON=img/none.svg
PYS60DIR=../PythonForS60
OPTS="--verbose --version=$1 --appname=\"$APPNAME\" --extrasdir=extras --heapsize=4k,5M --caps=$CAPBLS --icon=$ICON"

echo "Populating temp dir"

if [ -d $TMPDIR ]; then
    rm -fR $TMPDIR
fi

mkdir -p $TMPDIR/extras/data/python/milkshakedir/

cp -a $SRCDIR/lib/*       $TMPDIR/extras/data/python/milkshakedir/
cp -a $SRCDIR/plugins     $TMPDIR/extras/data/python/milkshakedir/
cp    $SRCDIR/default.py  $TMPDIR/

find $TMPDIR/ -name .svn -exec rm -fR {} \;

if [ ! -d ./module-repo/ ]; then
    cp -a $PYS60DIR/module-repo .
fi 

if [ ! -d ./templates/ ]; then
    cp -a $PYS60DIR/templates .
fi

if [ ! -f ensymble.py ]; then
    cp  $PYS60DIR/ensymble.py .
fi

$PYTHON ensymble.py py2sis $OPTS "$TMPDIR" "$APPNAME-$1.sis"

echo "Zipping source files"
tar --exclude=.svn -cvzf $APPNAME-$1-tar.gz src
zip -r $APPNAME-$1.zip src -x .svn

echo "Erasing"
rm -fR $TMPDIR

