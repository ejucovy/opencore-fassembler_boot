#!/bin/bash

# THIS SCRIPT DOES NOT TAKE CARE OF STOPPING OR CHECKING SERVICES!!!

# arguments:
# ./newbuild.sh profile_url basedir etc_svn_repo site_name base_port

BASEDIR="$2"

ETC_SVN_REPO="$3"

FASSEMBLER_EXTRAS_FILE="fassembler-req.txt"

INSTANCE="$4"

BASE_PORT="$5"

if [ `uname -s` == "Darwin" ]; then
	# Unfortunately BSD sed is not fully compatible with GNU sed.
	DB_PREFIX="$(echo ${INSTANCE%.*} | sed -E 's/[^a-zA-Z0-9_]+/_/g')_"
else
	DB_PREFIX="$(echo ${INSTANCE%.*} | sed -r 's/\W+/_/g')_"
fi
echo Database prefix normalized to "$DB_PREFIX"
	
REQ_BASE="https://svn.openplans.org/svn/build/requirements"
REQ_DIR="$1"
shift

if [ -z "$REQ_DIR" ] ; then
    echo "Usage: $(basename $0) REQ_DIR [fassembler options]"
    echo "REQ_DIR is a http(s) URL, or a directory at least two levels below $REQ_BASE"
    echo "Available:"
    svn cat https://svn.openplans.org/svn/scripts/build/list_req_dirs.py | python
    exit 2
fi

REQ_SVN=$REQ_DIR
if [[ $REQ_DIR != http://* && $REQ_DIR != https://* ]]; then
  REQ_SVN="$REQ_BASE/$REQ_DIR"
fi

svn ls $REQ_SVN &> /dev/null
if [ $? != 0 ]; then
    echo "The directory $REQ_SVN does not exist."
    echo "Available:"
    svn cat https://svn.openplans.org/svn/scripts/build/list_req_dirs.py | python
    exit 3
fi

cd ${BASEDIR}
cd builds

echo -n "refreshing fassembler-boot.py..."
svn export https://svn.openplans.org/svn/fassembler/trunk/fassembler-boot.py
echo "done."

DATE=$(date +%Y%m%d)

# check for build name
N=0
DIR="$DATE"
while [ -e "$DIR" ]
do
    N=$((N+1))
    DIR="$DATE-$N"
done

./fassembler-boot.py ${DIR}
cd $DIR

FASSEMBLER_EXTRAS="$REQ_DIR/$FASSEMBLER_EXTRAS_FILE"
svn export $FASSEMBLER_EXTRAS
if [ $? == 0 ]; then
    echo fassembler/bin/pip install -r $FASSEMBLER_EXTRAS_FILE
    fassembler/bin/pip install -r $FASSEMBLER_EXTRAS_FILE
fi

echo bin/fassembler base_port="$BASE_PORT" var="$BASEDIR/var" db_prefix=${DB_PREFIX} etc_svn_subdir=${INSTANCE} etc_svn_repo=${ETC_SVN_REPO} requirements_svn_repo="$REQ_SVN" fassembler:topp
bin/fassembler base_port="$BASE_PORT" var="$BASEDIR/var" db_prefix=${DB_PREFIX} etc_svn_subdir=${INSTANCE} etc_svn_repo=${ETC_SVN_REPO} requirements_svn_repo="$REQ_SVN" fassembler:topp

echo bin/fassembler etc_svn_subdir=${INSTANCE} etc_svn_repo=${ETC_SVN_REPO} missing 
bin/fassembler etc_svn_subdir=${INSTANCE} etc_svn_repo=${ETC_SVN_REPO} missing 
