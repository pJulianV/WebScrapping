import requests
import bs4
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url_asamblea='https://www.asambleanacional.gob.ec/es/contenido/transparencia-asamblea'

def status_code_url(url):
    r=requests.get(url)
    if r.status_code==200:
        s=BeautifulSoup(r.text, 'lxml')
    else:
        print('error no es correcto el status')
    return s

def links_anios(s):
    h5_year=s.find_all('h5')
    url_list=[completar_url(x.find('a').get('href')) for x in h5_year]
    return url_list


def link_months(url):
    s=status_code_url(url)
    h5_month=s.find_all('h5')
    meses=[completar_url(x.find('a').get('href')) for x in h5_month if x.find('a')]
    return(meses)

#identificar etiqueda li y luego verificar que contenga la palabar Viáticos

def links_pdf_viaticos(url):
    viaticos=[]
    s=status_code_url(url)
    links_pdf=s.find_all('li')
    for i in links_pdf:
        if 'Viáticos' in i.text:
            viaticos.append(completar_url(i.find('a').get('href')))
    return viaticos

def save_in_disk(url,i):
    r=requests.get(url)
    with open('pdf_download/file'+str(i)+'.pdf', 'wb') as f:
        f.write(r.content)


#funcion auxiliar parsear url
def completar_url(url):
    url_base='https://www.asambleanacional.gob.ec'
    return urljoin(url_base, url)


if __name__=='__main__':
    s=status_code_url(url_asamblea)
    anios=links_anios(s)
    meses =[]
    for x in anios:
        meses.append(link_months(x))
    meses_flaten=[x for item in meses for x in item]
    #print(meses_flaten)
    links_pdf=[]
    for x in meses_flaten:
        links_pdf.append(links_pdf_viaticos(x))
    flaten_pdf=[x for item in links_pdf for x in item]
 
    i=0
    while i<len(flaten_pdf):
        i+=1
        print(f'estoy descargando el link {i}')
        save_in_disk(flaten_pdf[i],i)

  