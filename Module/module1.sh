#! /bin/bash
for i in $(./module1_requete-google.sh $1) ; do ./module1_alchemyapi.sh $i;done
