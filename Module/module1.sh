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

# La requete
REQUETE=$1


for i in $(./module1_requete-google.sh ${REQUETE}) ; do 
	./module1_alchemyapi.sh $i;
done
