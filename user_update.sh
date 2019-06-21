#!/bin/bash

# Author: Wes Moskal-Fitzpatrick
#
# This script allows you to batch a number of tw user management options in one go.
#
# Change History:
#   20120202 : WMF : 1.0 : Created.

echo ""
ACTIVE=0
PASSWD=0
LIST=0
PASSOK=0
TWUSER=""

while getopts "aclpu:" opt; do
    case $opt in
        a) ACTIVE=1;;
        c) PASSWD=1;;
        l) LIST=1;;
        p) PASSOK=1;;
        u) TWUSER=$OPTARG;;
        :)  echo ""
            echo " How to use: mibtree_user.sh [ -aclp ] -u <user>"
            echo " Args:"
            echo "     -a : set active"
            echo "     -c : change password"
            echo "     -l : list user"
            echo "     -p : set password ok"
            echo ""
            ;;
    esac
done

if [ "$TWUSER" ]; then
    ARGS=0
    if [ "$LIST" = 1 ]; then
        ARGS=1
        tw_listusers | grep -i -A 5 $TWUSER
        echo ""
    fi
    if [ "$PASSWD" = 1 ]; then
        ARGS=1
        tw_passwd $TWUSER
        echo ""
    fi
    if [ "$PASSOK" = 1 ]; then
        ARGS=1
        tw_upduser --passwd-ok $TWUSER
        echo ""
    fi
    if [ "$ACTIVE" = 1 ]; then
        ARGS=1
        tw_upduser --active $TWUSER
        echo ""
    fi
    if [ "$ARGS" = 0 ]; then
        tw_listusers | grep -i -A 5 $TWUSER
        echo ""
    fi
else
    echo " How to use: user_update.sh [ -aclp ] -u <user>"
    echo " Args:"
    echo "     -a : set active"
    echo "     -c : change password"
    echo "     -l : list user"
    echo "     -p : set password ok"
    echo ""
fi
