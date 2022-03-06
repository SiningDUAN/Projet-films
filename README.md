# ***Web crawler***
## *Crawling le contenu du site web des films*
* Le principal axe de recherche de notre groupe est de crawling le site web des film. Nous essayons d'utiliser nos outils pour extraire des données sur les films, telles que la date de sortie, le réalisateur, les acteurs, les étoiles et le genre de chaque film. Les données extraites seront ensuite utilisées pour recommander des films aux utilisateurs et choisir leurs films préférés sans marcher sur le tonnerre.
* Il en va de même pour les autres sites web. On peut utiliser cette méthode pour explorer n'importe quel site web.

# *Environnement de dévéloppement*
* macOS or Linux or Windows
* python (3.6+)

# *Paguets de dépendances*
* requests

# ***Source des données***
## *Description des sources de données*
Le site de données du cinéma UGC à Strasbourg nous montre des informations instantanées sur tous les films qui sortent en salles à Strasbourg. 

## *Source des données pour ce projet*
Le lien vers les données spécifiques est le suivant:
https://www.ugc.fr/cinema.html?id=30

# *Mode d'emploi*
Cet outil se compose de deux scripts:
1. ***data.py***
 - La fonction *clean* est définie dans *data.py* pour l'outil d'extraction du code source *html* de l'outil.
 - La fonction *clean* extrait : le titre du film, la note, la catégorie du film, le réalisateur, l'acteur et le synopsis via deux modules, *beautifulsoup* et *re*.
```Python
from bs4 import BeautifulSoup
import re
```
```Python
def clean(text):
    soup =  BeautifulSoup(text, 'html.parser')
    soup.find_all('div', class_= "info-wrapper main")
    #get grade
    content = soup.find_all('ul', class_ = 'no-bullets film-score color--main-blue d-none')
    grade = len(re.findall("plein", str(content)))
    #get title
    title = soup.find('h1', class_ = 'block--title color--dark-blue text-uppercase').text
    #get publication date
    contents=soup.find_all('p', class_ = 'color--grey')
    date,director,actors=None,None,None
    for content in contents:
        #print(content.text)
        #La date de sortie
        if 'Sortie le' in content.text:
            part_2_content=content.find_all('span')
            # print(part_2_content)
            date = part_2_content[0].text
            # type = part_2_content[1].text
        #Directeur
        if re.findall(r'\bDe\b', content.text):
            director = content.find('span').text
        #Acteur
        if re.findall(r'\bAvec\b', content.text):
            actors = content.find('span').text
    #synopsis
    synopsis_div = soup.find_all('div', class_ = 'group-info d-none d-md-block')
    for div in synopsis_div:
        if 'Synopsis' in div.text:
            synopsis = div.find('p',class_='color--dark-blue').text
    # print(synopsis_div)
    #type
    type=soup.find('p', class_ = 'color--dark-blue').text
    return grade,title,date,type,director,actors,synopsis
```    
2. ugc.fr.py
 - C'est le programme principal de l'outil, qui définit une classe UGC, principalement utilisée pour récupérer les liens vers les films depuis ugc.fr et pour obtenir les détails *html* de chaque film.
 - La fonction *main*, qui est la fonction d'exécution de la classe UGC, appelle respectivement les fonctions suivantes:
    (1) fonction *get_links* : ouvrir https://www.ugc.fr/cinema.html?id=30 via *selenium* et récupère tous les liens vers le film.
    (2) Chaque lien de film obtenu via *get_links* est donné à la fonction *get_info*, qui ouvrira le lien du film avec le module *requests* et récupérera le code source *HTML*.
    (3) Le code source *html* obtenu à partir de *get_info* est donné à la fonction *clean* de data.py, qui est utilisée pour extraire les informations du film.
    (4) Une fois que toutes les informations sur les films ont été extraites, la fonction *save_data* stocke les données dans le fichier *results.csv*.
  
```Python  
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import csv
from data import clean
```
```Python
class UGC():
    PATH = './chromedriver.exe'

    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    
    req_driver=requests.session()
    req_driver.headers={
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5',
        'cache-control': 'max-age=0',
        'cookie': 'serverName=www.ugc.fr; buildVersion=572629e4c92e1276c73a26e1a10b3e3f; lang=fr; ugcReservationId=; ugcReservationSeanceId=; ugcOperationCarteAchatId=; ugcSearchText=; ugcNbResultSearch=; WW_TRANS_I18N_LOCALE=fr; didomi_token=eyJ1c2VyX2lkIjoiMTdmNTdhMjktNTU1OC02MmNjLTg4YWItZmIyMjY3NWM4M2YwIiwiY3JlYXRlZCI6IjIwMjItMDMtMDVUMDE6MTI6MzUuNTIxWiIsInVwZGF0ZWQiOiIyMDIyLTAzLTA1VDAxOjEyOjM1LjUyMVoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpjb250ZW50c3F1YXJlIiwiYzphYnRhc3R5Mi1pempKUk1FaSIsImM6Z29vZ2xlYW5hLTRUWG5KaWdSIiwiYzphZGR0aGlzLTRiZlVLcXpWIiwiYzp1Z2MtSE1rQ3pZM2oiLCJjOnByZWhvbWV1LWJKMzhycXozIiwiYzpzbWFydHRyaWItd0J3Q3dVdHkiXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsiYWRkdGhpc3AtaU5CMzM5UXgiLCJwcmVob21lLUp5VllNQVU5IiwiZGV2aWNlX2NoYXJhY3RlcmlzdGljcyIsImdlb2xvY2F0aW9uX2RhdGEiXX0sInZlbmRvcnNfbGkiOnsiZW5hYmxlZCI6WyJnb29nbGUiXX0sInZlcnNpb24iOjJ9; euconsent-v2=CPVWpAAPVWpAAAHABBENCECsAP_AAH_AAAqIIltf_X__b3_j-_5_f_t0eY1P9_7_v-0zjhfdt-8N3f_X_L8X42M7vF36pq4KuR4Eu3LBIQdlHOHcTUmw6okVrzPsbk2cr7NKJ7PEmnMbO2dYGH9_n93TuZKY7______z_v-v_v____f_7-3_3__5_3---_e_V_99zLv9____39nP___9v-_9_____4IhgEmGpeQBdiWODJtGlUKIEYVhIdAKACigGFoisIHVwU7K4CfUELABCagIwIgQYgowYBAAIBAEhEQEgB4IBEARAIAAQAqwEIACNgEFgBYGAQACgGhYgRQBCBIQZHBUcpgQESLRQT2ViCUHexphCGWWAFAo_oqEBEoQQLAyEhYOY4AkBLhZIFmKF8gAAAAA.f_gAD_gAAAAA; advertisingCampaign247Cookie=1; ugcCinemaId=; ugcCinemaCode=; JSESSIONID=4E23E029EA509AED9623B5432E79F0CA.tomcat04; currentCinemaId=; url=https%3A%2F%2Fwww.ugc.fr%2FfilmAction%3Fpage%3D30008; ugcPageId=30008; ugcFilmId=',
        'dnt': '1',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Microsoft Edge";v="98"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.62',
    }
```
```Python
    def get_links(self):
        driver = webdriver.Chrome(self.PATH,chrome_options=self.chrome_options)           
        links = []
        driver.get('https://www.ugc.fr/cinema.html?id=30') 

        WebDriverWait(driver,30).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="didomi-notice-agree-button"]'))
        ).click()

        elems = driver.find_elements_by_xpath("//a[@href]")

        for elem in elems:
            links.append(elem.get_attribute("href"))

        links = {link for link in links if 'film.html?id=' in link}
        links = list(links)
        driver.quit()
        return links

    def get_info(self,link): 
        req = self.req_driver.get(link)
        grade,title,date,type,director,actors,synopsis=clean(req.text)
        return grade,title,date,type,director,actors,synopsis
    
    def save_data(self,results):
        with open('result.csv','w',newline='',encoding='utf-8-sig') as f:
            writer=csv.writer(f)
            writer.writerow(['title','grade','date','type','director','actiors','synopsis'])
            writer.writerows(results)
           
    def main(self):
        start_time=time.perf_counter()
        links = self.get_links()
        results=[]
        for link in links:
            grade,title,date,type,director,actiors,synopsis = self.get_info(link)
            print(f'getting info from {link}->title:{title},grade:{grade}')
            results.append([title,grade,date,type,director,actiors,synopsis])
        self.save_data(results)
        end_time=time.perf_counter()
        print(f'Finished in {round(end_time-start_time,2)} seconds')

if __name__=='__main__':
    ugc = UGC()
    ugc.main()

 ```   

# *Conclusion*
* Le type de *drame* obtient un nombre d'étoiles plus élevées
* Les films qui sont sortis relativement tôt ont été mieux reçus

# *Applications*
* Par ces données, on peut obtenir l'information clairement de chaque film
* On peut utiliser ce méthode qui s'applique aussi aux autres sites

# *Remerciements spéciaux*
* CSDN: une site nous permet de chercher la code
* le professeur nous aide beaucoup sur la code
