from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os

from selenium.webdriver.chrome.options import Options

#User Defined Parametres
url="" #add base url here
file_name="physiotherapists_banglore.csv"
pages_to_scroll=20

#Lists for storing name, address, contact number
nameList = []
addressList = []
numbersList = []
reviewList = []
pageList = []

#Scroll through all pages
for num in range(1,pages_to_scroll+1):
    #Open chrome driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    url1=url+"/page-"+str(num)
    driver.get(url1)
    time.sleep(2)
    #Get information of all phsiotherapists 
    storeDetails = driver.find_elements(By.CLASS_NAME,'store-details')

    
    #Iterate through each physiotherapist
    for i in range(len(storeDetails)):
        #Get name and address
        name = storeDetails[i].find_element(By.CLASS_NAME,'lng_cont_name').text
        address = storeDetails[i].find_element(By.CLASS_NAME,'cont_fl_addr').get_attribute('innerHTML')
        reviews = storeDetails[i].find_element(By.CLASS_NAME,'green-box').text
        #Store name and address
        nameList.append(name)
        addressList.append(address)
        reviewList.append(reviews)
        pageList.append(num)
    #Close browser 
    driver.close()


#Store data to dataframe
data = {'Name':nameList,
            'Address': addressList}
df = pd.DataFrame(data)


driver = webdriver.Chrome(ChromeDriverManager().install())

for ind in df.index:
    #Create a url for name and address
    name=df['Name'][ind]+df['Address'][ind]
    name=name.split(' ')
    name='+'.join(name)
    url="https://www.google.com/search?q="+name

    driver.get(url)
    time.sleep(2)
    Details = driver.find_elements(By.CLASS_NAME,'wDYxhc')
    contact=''
    #Search for contact number
    for i in Details:
        contact=''
        try:
            contact_number=i.find_element(By.CLASS_NAME,"Z1hOCe").text
            elements=contact_number.split(' ')
            if(elements[0]=="Phone:"):
                contact=' '.join(elements[1:])
                break
        except:
            continue
    numbersList.append(contact)

#Add all data to dataframe
data = {'Company Name':nameList,
        'Address': addressList,
        'Contact': numbersList,
        'Reviews':reviewList,
        'Page Number':pageList}
df = pd.DataFrame(data)

#Save the file
df.to_csv(file_name, header=["Name","Address","Contact Number","Reviews","Page Number"], index=False)