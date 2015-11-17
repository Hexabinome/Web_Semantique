import json
input_file=open('testrdf.json', 'r')
output_file=open('testoutput.json', 'w')

json_decode=json.load(input_file)


result = []
for item in json_decode:
    my_dict={}
    my_dict['title']=item.get('labels').get('en').get('value')
    my_dict['description']=item.get('descriptions').get('en').get('value')
    my_dict['id']=item.get('id')
    print my_dict
    result.append(my_dict)

back_json=json.dumps(result, output_file)

output_file.write(back_json)
output_file.close() 


print"Hello world"