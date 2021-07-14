import os
import subprocess
import json

def getNamespaces(includeDefault=0):
	out = subprocess.Popen(['kubectl', 'get', 'namespaces', '-o', 'json'], 
		       stdout=subprocess.PIPE, 
		       stderr=subprocess.STDOUT)
	stdout,stderr = out.communicate()
	outjson = json.loads(stdout)
	ls_namespaces=[]
	if includeDefault:
		ls_namespaces.append("default")
	for i in outjson['items']:
		if not (  (i['metadata']['name']).startswith("kube") or i['metadata']['name']=='default'):
			ls_namespaces.append(i['metadata']['name'])
	return ls_namespaces

def getServices(namespace):
	out = subprocess.Popen(['kubectl', 'get', 'services', '-n', namespace, '-o', 'json'], 
		       stdout=subprocess.PIPE, 
		       stderr=subprocess.STDOUT)
	stdout,stderr = out.communicate()
	outjson = json.loads(stdout)
	ls_services=[]
	for i in outjson['items']:
		ls_services.append(i['metadata']['name'])
	return ls_services

def getDeployments(namespace):
	out = subprocess.Popen(['kubectl', 'get', 'deployments', '-n', namespace, '-o', 'json'], 
		       stdout=subprocess.PIPE, 
		       stderr=subprocess.STDOUT)
	stdout,stderr = out.communicate()
	outjson = json.loads(stdout)
	ls_deployments=[]
	for i in outjson['items']:
		ls_deployments.append(i['metadata']['name'])
	return ls_deployments

def deleteDeployments(namespace):
	out = subprocess.Popen(['kubectl', 'get', 'deployments', '-n', namespace, '-o', 'json'], 
		       stdout=subprocess.PIPE, 
		       stderr=subprocess.STDOUT)
	stdout,stderr = out.communicate()
	outjson = json.loads(stdout)
	for i in outjson['items']:
		print("\t$kubectl delete deployments -n " + namespace + " " + i['metadata']['name'])
		os.system("kubectl delete deployments -n " + namespace + " " +i['metadata']['name'])
	return 1

def deleteServices(namespace):
	out = subprocess.Popen(['kubectl', 'get', 'services', '-n', namespace, '-o', 'json'], 
		       stdout=subprocess.PIPE, 
		       stderr=subprocess.STDOUT)
	stdout,stderr = out.communicate()
	outjson = json.loads(stdout)
	for i in outjson['items']:
		if i['metadata']['name'] == 'kubernetes':
			return 0
		print("\t$kubectl delete services -n " + namespace + " " + i['metadata']['name'])
		os.system("kubectl delete services -n " + namespace + " " +i['metadata']['name'])
	return 1

def deleteNamespace(namespace):
	print("\t$kubectl delete namespaces " + i)
	os.system("kubectl delete namespaces " + i)
	return 1

def main():
	for i in getNamespaces(includeDefault=1):
		print("Services in namespace: ",i)
		print(getServices(i))

	for i in getNamespaces(includeDefault=1):
		print("Deployments in namespace: ",i)
		print(getDeployments(i))

	print("Deleting Deployments...")
	for i in getNamespaces(includeDefault=1):
		print("Deleting deployments in namespace: ",i)
		deleteDeployments(i)
		print()
		
	print("Deleting Services...")
	for i in getNamespaces(includeDefault=1):
		print("Deleting services in namespace: ",i)
		deleteServices(i)
		print()

	print("Deleting Namespaces...")
	for i in getNamespaces():
		print("Deleting namespace: ",i)
		deleteNamespace(i)
		print()
	print("kubernetes service in default namespace has not been deleted.")
if __name__ == "__main__":
    main()
