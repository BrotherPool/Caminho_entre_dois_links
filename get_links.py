from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
import time
import sys
import functools


def progbar(curr,filhos,tempo, total=100, full_progbar=20):
    frac = curr/total
    filled_progbar = round(frac*full_progbar)
    print('\r', "Progresso: "+'#'*filled_progbar + '-'*(full_progbar-filled_progbar), '[{:>7.2%}]'.format(frac)," Filhos: %d Tempo: %.2f segundos"%(filhos,tempo), end='')
 
    
def getLinks(url):
    req = urllib2.Request(url, headers={'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"})
    try:
        html_page = urllib2.urlopen(req).read()
        soup = BeautifulSoup(html_page, "html.parser",from_encoding="iso-8859-1")
        links = []
        possible_links = soup.find_all()
        for link in possible_links:
            if link.has_attr('href'):
                aux=link.attrs['href']
                if aux is not None:
                    aux2=aux.split(':')
                    if(aux2[0]=="https" or aux2[0]=="http"):
##                        decisao=adiciona_ou_nao_filho(aux)
##                        if(decisao==True or aux==site_alvo):
                            links.append(aux)
        links=list(set(links))
        links.sort()
        return links
    except:
        return None

def get_caminho_pai(filho):
    caminho=[]
    caminho.append(filho.get_nome_do_site())
    pai=filho.get_pai()
    while(pai is not None):
        caminho.append(pai.get_nome_do_site())
        pai=pai.get_pai()
    return caminho

##print( getLinks("https://jovemnerd.com.br") )


def adiciona_ou_nao_filho(link):
    for site in lista_de_sites:
        filhos=site.get_filhos()
        if filhos is not None:
            for filho in filhos:
                if filho==link:
##                    print("Não add")
                    return False
##    print("add")
    return True

class Node:
    def __init__(self, altura,altura_max, nome_do_site,pai=None):
        self.nome_do_site = nome_do_site
        if(altura_max==-1):
            if(altura<max_height):
                self.filhos = getLinks(nome_do_site)
            else:
                self.filhos=None
        else:
            if(altura<altura_max-1):
                self.filhos = getLinks(nome_do_site)
            else:
                self.filhos=None
        self.pai=pai
    
    def get_filhos(self):
        return self.filhos
    def get_nome_do_site(self):
        return self.nome_do_site
    def get_pai(self):
        return self.pai

lista_de_sites=[]
menor_caminho=[]
lista_achou=[]
altura_menor=-1
porcentagem=0
porcento=0
filhos_acessados=0
##site_pai="https://stackoverflow.com/questions/24945813/python-printing-in-the-same-exact-spot-using-r-not-working"
##site_alvo="https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console"
##max_height=2
site_pai=str(input("Digite a url de inicio: "))
site_alvo=str(input("Digite a url de destino: "))
max_height=int(input("Digite a quantidade de pulos máximos entre links: ")) #profundidade máxima da árvore
lista_de_alturas=range(max_height)


@functools.lru_cache(maxsize=128)
def recursao(altura,site,pai=None):
    
    global lista_achou,altura_menor,menor_caminho,porcentagem,porcento,filhos_acessados
##    progbar(porcentagem,filhos_acessados,time.time() - start)
    if(altura==1):
        porcentagem=porcentagem+porcento
        progbar(porcentagem,filhos_acessados,time.time() - start)
    if altura<altura_menor or altura_menor==-1:
        if(pai==None):
            new_node=Node(altura,altura_menor,site)
            quantidade=len(new_node.get_filhos())
            porcento=100/quantidade
            porcentagem=porcentagem+porcento
        else:
            new_node=Node(altura,altura_menor,site,pai)
        if(new_node not in lista_de_sites):
            lista_de_sites.append(new_node)
            filhos=new_node.get_filhos()
            
##            print("Altura na árvore: "+str(altura))
##            print("Nome do Site: "+str(new_node.get_nome_do_site()))
    ##        print("Filhos: "+str(new_node.get_filhos()))
    ##        print("\n\n")
##            print(altura,end="")
            if(new_node.get_nome_do_site()==site_alvo):
                print("\n\n.....ACHOU ALGO NA ALTURA "+str(altura))
                menor_caminho=get_caminho_pai(new_node)
                print("\n\n")
                lista_achou.append(altura)
                altura_menor=min(lista_achou)
            else:
                if(altura_menor==-1):
                    if altura<max_height:
                        if filhos is not None:
                            for filho in filhos:
                                filhos_acessados=filhos_acessados+1
                                progbar(porcentagem,filhos_acessados,time.time() - start)

        ##                        print(filho)
                                recursao(altura+1,filho,new_node)
                else:
                    if altura<altura_menor:
                        if filhos is not None:
                            for filho in filhos:
        ##                        print(filho)
                                filhos_acessados=filhos_acessados+1
                                progbar(porcentagem,filhos_acessados,time.time() - start)
                                recursao(altura+1,filho,new_node)
        return menor_caminho 

start = time.time()
menor=recursao(0,site_pai)
if(menor==[]):
    print ("\nNão é possivel achar o site alvo com apenas %d pulos" %max_height)
else:
    menor.reverse()
    print("\nMenor caminho é: "+str(menor)+" precisando no mínimo de "+str(len(menor)-1)+" pulos")
##    end = time.time()
##    print("Tempo até achar o site: %d segundos" %(end - start))

input("Precione Enter para continuar")
