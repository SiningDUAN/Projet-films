# Projet: données du site web du film

# Exigences environnementales
> macOS or Linux or Windows
> python (3.6+)
> pip

# Source des données
## Description des sources de données 
Pour réaliser notre projet, on utilise le site de données du cinéma UGC à Strasbourg
## Source des données pour ce projet
Le lien vers les données spécifiques est le suivant:

# Fichiers de configuration
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from bs4 import BeautifulSoup
import re
#Le chemin jusqu'au chromedriver
PATH = "/Users/zhangyajie/Downloads/chromedriver 2"

#On précise certaines option
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(PATH,chrome_options=chrome_options)

#Ouverture de la page web
driver.get('https://www.ugc.fr/cinema.html?id=30') 

#On clique sur 'continue without agreeing'
driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/div/span").click()
##On cherche maitnenant tout les liens du film sur la page
#on crée une liste vide
links = []
#On récupère tout les éléments avec des href (les liens) 
elems = driver.find_elements_by_xpath("//a[@href]")
#on ajoute chaque lien a une liste
for elem in elems:
    links.append(elem.get_attribute("href"))

#On vérifie qu'il y a bien 'film.htlm?id=' dans le lien, puisque seul ces liens la sont pour un film disponible
links = {link for link in links if 'film.html?id=' in link}
links = list(links)
links
###définition d'une fonction get_grade de chaque lien dans la liste de links
def get_grade(link): 
        
    req = requests.get(link)
    soup =  BeautifulSoup(req.text, 'html.parser')
    soup.find_all('div', class_= "info-wrapper main")
    content = soup.find_all('ul', class_ = 'no-bullets film-score color--main-blue d-none')
    grade = len(re.findall("plein", str(content)))
    return grade

###print tous les liens et les notes d'un file qui est en format de lien 
for link in links:
    grade = get_grade(link)
    print((link,grade))
    

###CHERCHER LE MEILLEUR FILM:
def best_film(link):
    
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'html.parser')
    soup.find_all('div', class_= "info-wrapper main")
    content = soup.find_all('ul', class_ = 'no-bullets film-score color--main-blue d-none')
    grade = len(re.findall("plein", str(content)))
    return grade
    
for link in links:
    grade = best_film(link)
    best = sorted(grade,reverse=True)  # je veux faire un ordre décroissant avec le 'grade' définit, mais le résultat me montre "TypeError: 'int' object is not iterable"
    print((link,best))



###CHERCHER LE NOM DES FILMS:
    
def get_name(link):
    
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'html.parser') 
    soup.find_all('div', class_ = "info-wrapper main") ## trouver tous les 'div' avec class = "info-wrapper main" 
    content = soup.find_all('h1', class_ = 'class="block--title color--dark-blue text-uppercase"') # sous soup.find_all, on cherche tous les 'h1' avec class = ...
    name = re.findall('<h1 class="block--title color--dark-blue text-uppercase>(.*?)</h1>', str(content)) # chercher les contenus entre <h1...> et le premier </h1>
    return name


for link in links:
    name = get_name(link)
    grade = get_grade(link)
    print((link,name,grade)) # les noms sont vides
# Format des données 

# Mode d'emploi

# Liste des fonctions
> Recherche d'informations sur les sites de cinéma UGC et sauvegarde dans la bibliothèque

# Remerciements spéciaux
