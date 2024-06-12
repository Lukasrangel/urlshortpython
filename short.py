#!/usr/bin/python

import argparse
import requests

##constants
API_KEY="sk_MHHnuUEd7QWqgZGR"
DOMAIN="fhtb.short.gy"
API_LINK_BASE="https://api.short.io"

HEADERS = {
      'authorization': API_KEY,
      'content-type': 'application/json'
}


def args():
	parser = argparse.ArgumentParser(prog='urlShort', description='Encurtador de URLs')
	parser.add_argument('-l', '--link', help='URL para encurtar')
	parser.add_argument('-s', '--show',action='store_true', help='Mostrar seus links criados')
	parser.add_argument('-d', '--delete', dest='id', help='Deletar shortlink com base no id')
	return [parser.parse_args(), parser]



def switch(args, HEADERS) :
	if args.link: create_short_link(HEADERS, args.link)
	elif args.show: show_links(HEADERS)
	elif args.id: delete(HEADERS, args.delete)
	else: parser.print_help()




def get_domain_id(HEADERS):
	url = API_LINK_BASE+"/api/domains"

	req = requests.get(url, headers=HEADERS)

	if req.status_code == 200:
		return req.json()[1]['id']
	else:
		return None

def create_short_link(HEADERS, link):
	req = requests.post(API_LINK_BASE+'/links', json={
		'domain': DOMAIN,
		'originalURL' : link
	}, headers=HEADERS)

	print(req.status_code)
	if req.status_code == 200:
		print("Link Criado!")
		print(req.json())
	else:
		print('Use um link válido!')
		return False

def count_clicks(HEADERS, linkId):
	url = "https://statistics.short.io/statistics/domain/{}/link_clicks".format(get_domain_id(HEADERS))

	req = requests.get(url, headers=HEADERS, params={
		'ids' : linkId
	})

	return req.json()[linkId]


def show_links(HEADERS) :
	domain_id=get_domain_id(HEADERS);

	url = "https://api.short.io/api/links?dateSortOrder=desc"

	req = requests.get(url, headers=HEADERS, params={
		'domain_id' : domain_id,
		'limit' : 30
	})

	if req.status_code == 200:
		print("Sua lista de links! \n\n")
		links = req.json()['links']
		for link in links:
			print("Criado em {}".format(link['createdAt']))
			print("id: " + link['id'])
			print("URLshort: " + link['shortURL'])
			print("URLoriginal: " + link['originalURL'])
			print("Numero de clicks: {}".format(count_clicks(HEADERS, link['id'])) )
			print("\n \n \n")
	else:
		print('Alugm erro ocorreu')



def delete(HEADERS, id) :
	url = API_LINK_BASE + "/links/" + id

	req = requests.delete(url, headers=HEADERS)

	if(req.status_code == 200):
		print("Short Link deletado")
	else:
		print("Id não encontrado")

	


if __name__=="__main__":
	args, parser = args()
	switch(args, HEADERS)
	
	