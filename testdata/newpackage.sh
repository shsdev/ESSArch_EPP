#!/bin/bash
if [ $# -lt 1 ]; then
    echo "usage: newpackage.sh <new_id>"
    exit 1;
fi
OLD_ID=96b68052-2489-11e5-b6bf-fa163e879c37
LOBBY_ID=55be5142-24d9-11e5-88aa-fa163e879c37
NEW_ID=$1

# working dir
WDIR=/opt/python_wsgi_apps/ESSArch_EPP/testdata

# clean up
cd $WDIR
rm -rf cd usb lobby
tar -xvf test_ip1_path_gate.tar
tar -xvf test_ip1_path_reception.tar

if [ -f cd/${OLD_ID}.tar ]; then
    echo "IP file found"
else
    echo "Error: IP file not found at path: cd/${OLD_ID}.tar"
    exit 1
fi


cd $WDIR/lobby/$LOBBY_ID/$OLD_ID/content/
tar xvf $OLD_ID.tar
rm $OLD_ID.tar

# replace identifier
find $WDIR/lobby -type f -exec sed -i "s/${OLD_ID}/${NEW_ID}/g" {} \; 
find $WDIR/lobby -type f -exec sed -i "s/${LOBBY_ID}/${NEW_ID}/g" {} \; 
 
# package lobby content IP
mv $OLD_ID $NEW_ID
tar -pcf $NEW_ID.tar $NEW_ID
rm -rf $NEW_ID

cd $WDIR
mv lobby/$LOBBY_ID/$OLD_ID lobby/$LOBBY_ID/$NEW_ID
mv lobby/$LOBBY_ID lobby/$NEW_ID

# delete old tar
cd $WDIR/cd
tar -xvf ${OLD_ID}.tar
rm ${OLD_ID}.tar

find $WDIR/cd -type f -exec sed -i "s/${OLD_ID}/${NEW_ID}/g" {} \; 
find $WDIR/cd -type f -exec sed -i "s/${LOBBY_ID}/${NEW_ID}/g" {} \;

# rename folder
mv ${OLD_ID} ${NEW_ID}

# package new IP
tar -pcf ${NEW_ID}.tar ${NEW_ID}/
rm -rf ${NEW_ID}

cd $WDIR

# copy to epp
cp -r lobby/${NEW_ID} /var/data/ESSArch/exchange/lobby/
cp cd/${NEW_ID}.tar /var/data/ESSArch/reception/cd/
