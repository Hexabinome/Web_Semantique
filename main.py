import subprocess
from Module import module3


# call module 1 REQUEST TO URL TO TEXT URL
subprocess.check_call(['./Module/module1.sh'])
f = open('Module/output/alchemy.json')

# call module 2 TEXT URL TO URI TO RDF
module3.function('Module/output/alchemy.json')

# call module 3 RDF TO RESULTS
