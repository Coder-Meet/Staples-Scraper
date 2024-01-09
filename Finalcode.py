from selenium import webdriver
from bs4 import BeautifulSoup
import csv,time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options



options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
data = []
with open("mfgpn.csv","r") as file:
    
    csvreader = csv.reader(file,delimiter=":")
    for row in csvreader:
        if len(row) > 4:
            pass
        else:
            data.append(row)
            

data.pop(0)


url = f"https://www.staples.ca/search?query=CL-41"
driver.get(url)
time.sleep(1)

driver.set_page_load_timeout(10)


for count,product in enumerate(data):
    
    mfgnm = product[2]

    if "DPC" in mfgnm:
        mfgnm = mfgnm.removeprefix('DPC')
    
    driver.find_element_by_xpath('//*[@id="algoliasearch-searchbar-input"]').send_keys(Keys.BACK_SPACE*15)
    driver.find_element_by_xpath('//*[@id="algoliasearch-searchbar-input"]').send_keys(mfgnm)
    driver.find_element_by_xpath('//*[@id="algoliasearch-searchbar-input"]').send_keys(Keys.ENTER)
    
    time.sleep(0.2)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    price = soup.find("span", class_="money pre-money")
    description = soup.find("a", class_="product-thumbnail__title product-link")
    num_products = soup.find_all('div', class_='ais-hits--item')
    
    if len(num_products)>1:
        
        description = "Multiple products"

    if price:
        if type(price) != str:
            price = price.text
    
    if description:
        if type(description) != str:
            description = description.text.replace('"','')
            description.replace("'",'')
    
    if description!=None:
        data[count].append(price)
    data[count].append(description)
    
    #print(price)
    #print(description)
    #print(len(num_products))

with open('Staples Stock.txt','w',newline='') as f:
    writer = csv.writer(f,delimiter=':')
    writer.writerows(data)
    f.close()

driver.quit()

#_____________________________________________________________________________________________________________________________________________________________________
driver = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
url = f"https://www.staples.ca/search?query=CL-41"
driver.get(url)
time.sleep(1)

driver.set_page_load_timeout(10)

print("___________________________________________________________________________________________________________________________________________________")
print("Which product matches the following discription (Enter the number, count starts at 1, enter 0 to indicate none match):")
for count,product in enumerate(data):
    
    if len(product)>5:
        if product[5] == "Multiple products":
            
            mfgnm = product[2]

            if "DPC" in mfgnm:
                mfgnm = mfgnm.removeprefix('DPC')
            
            driver.find_element_by_xpath('//*[@id="algoliasearch-searchbar-input"]').send_keys(Keys.BACK_SPACE*15)
            driver.find_element_by_xpath('//*[@id="algoliasearch-searchbar-input"]').send_keys(mfgnm)
            driver.find_element_by_xpath('//*[@id="algoliasearch-searchbar-input"]').send_keys(Keys.ENTER)
            
            time.sleep(0.3)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            
            choice = input(f"{product[1]}\n-->")
            while type(choice) != int:
                try:
                    choice = int(choice) 
                except:
                    choice = input(f"{product[1]}\n-->")

            if choice == 0:
                price1 = "None Matched"
                description1 = 'None Matched'
            else:
                
                try:
            
                    for y in soup.find_all('div', class_='ais-hits--item')[choice-1].find_all('span'):
                        
                        if '$' in y.text:
                            price1 = y.text
                            
                    description1 = soup.find_all("a", class_="product-thumbnail__title product-link")[choice-1].text
                    
                except:
                    print(f"Unable to extract data of product {choice}")
                    price1 = "None Matched"
                    description1 = 'None Matched'
            
            data[count][4] = price1
            data[count][5] = description1
            

driver.quit()

with open('Staples Stock.txt','w',newline='') as f:
    writer = csv.writer(f,delimiter=':')
    writer.writerows(data)
    f.close()
    
