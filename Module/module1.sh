#! /bin/bash
# Usage : module1.sh "requete" nbResultat


#Verification du nombre d'arguments qui doit valoir 1
NBARGS=$#

if ! [ ${NBARGS} -eq 2 ]; then
	echo "Nombre d'arguments incorrects. Il faut la requete en paramètre et le nombre de resultats."
	echo "Example : module1.sh dexter 10."
	#statements
	exit 123
fi

OUTPUTFILE="Module/output/alchemy.json"

# La requete
REQUETE=$1
NBRES=$2

echo "{ \"resultats\" :" > ${OUTPUTFILE}

for i in $(Module/module1_requete-google.sh ${REQUETE} ${NBRES}) ; do
	Module/module1_alchemyapi.sh $i ;
done | jq -s '.' >> ${OUTPUTFILE}

echo "}" >> ${OUTPUTFILE}