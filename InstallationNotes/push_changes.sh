#!/bin/bash

# Synchronize the files from workspace with the active web site
FROM_ENV=$1

if [ $2 = "DEV" ] ; then
	TO_ENV="/path/to/integration/environment/python/polarCommonProj/"
	TO_WSGI="/path/to/integration/environment/python/wsgi"
elif [ $2 = "TEST" ] ; then
	TO_ENV="/path/to/qa/environment/python/polarCommonProj/"
	TO_WSGI="/path/to/qa/environment/python/wsgi"
elif [ $2 = "WEB" ] ; then
	TO_ENV="/path/to/production/environment/python/polarCommonProj/"
	TO_WSGI="/path/to/production/environment/python/wsgi"
elif [ $2 = "PROD" ] ; then
	TO_ENV="/path/to/production/environment/python/polarCommonProj/"
	TO_WSGI="/path/to/production/environment/python/wsgi"
else
	TO_ENV="/disks/www/$2/APPS/python/polarCommonProj/"
	TO_WSGI="/disks/www/$2/APPS/python/wsgi"	
fi

if [ "$FROM_ENV" = "SVN" ] ; then
    FROM_ENV="./trunk/polarCommonProj/"
    FROM_WSGI="./trunk/polarCommonProj/InstallationNotes"
    PIC_WSGI=$FROM_WSGI
    API_WSGI=$FROM_WSGI
elif [ "$FROM_ENV" = "DEV" ] ; then
    FROM_ENV="/path/to/integration/environment/python/polarCommonProj/"
    FROM_WSGI="/path/to/integration/environment/python/wsgi"
    PIC_WSGI="$FROM_WSGI/polarCommonProj"
    API_WSGI="$FROM_WSGI/picbadgeapi"
elif [ "$FROM_ENV" = "TEST" ] ; then
    FROM_ENV="/path/to/qa/environment/python/polarCommonProj/"
    FROM_WSGI="/path/to/qa/environment/python/wsgi"
    PIC_WSGI="$FROM_WSGI/polarCommonProj"
    API_WSGI="$FROM_WSGI/picbadgeapi"
elif [ "$FROM_ENV" = "WEB" ] ; then
    FROM_ENV="/path/to/production/environment/python/polarCommonProj/"
    FROM_WSGI="/path/to/production/environment/python/wsgi"
    PIC_WSGI="$FROM_WSGI/polarCommonProj"
    API_WSGI="$FROM_WSGI/picbadgeapi"
elif [ "$FROM_ENV" = "PROD" ] ; then
	FROM_ENV="/path/to/production/environment/python/polarCommonProj/"
    FROM_WSGI="/path/to/production/environment/python/wsgi"
    PIC_WSGI="$FROM_WSGI/polarCommonProj"
    API_WSGI="$FROM_WSGI/picbadgeapi"
else 
    FROM_ENV="/disks/www/$1/APPS/python/polarCommonProj/"
    FROM_WSGI="/disks/www/$1/APPS/python/wsgi"
    PIC_WSGI="$FROM_WSGI/polarCommonProj"
    API_WSGI="$FROM_WSGI/picbadgeapi"
fi 

rsync -a --exclude .svn  --delete $FROM_ENV $TO_ENV

# copy wsgi file 
# This causes the server to refresh/restart with the new configuration
cp $PIC_WSGI/polarCommonProj.wsgi  $TO_WSGI/polarCommonProj/polarCommonProj.wsgi
cp $API_WSGI/picbadgeapi.wsgi  $TO_WSGI/picbadgeapi/picbadgeapi.wsgi
