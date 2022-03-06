from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import csv
from data import clean


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