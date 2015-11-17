#! /bin/bash
# Usage : module1.sh "requete"


#Verification du nombre d'arguments qui doit valoir 1
NBARGS=$#

if ! [ ${NBARGS} -eq 1 ]; then
	echo "Nombre d'arguements incorrects. Il faut juste la requete en paramètre."
	echo "Example : ..."
	#statements
	exit 123
fi

OUTPUTFILE="Module/output/alchemy.json"

# La requete
REQUETE=$1

echo "{ resultats :[" > ${OUTPUTFILE}

for i in $(Module/module1_requete-google.sh ${REQUETE}) ; do 
	Module/module1_alchemyapi.sh $i >> ${OUTPUTFILE};
done


echo ] >> ${OUTPUTFILE}