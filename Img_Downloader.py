from selenium import webdriver
import os
import requests
import pyautogui#may not need
import time#may not need
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#function to download image
def save_img(url, path, rf_url):

    #credentials for entry if necessary
    headers = {
        #mimics popular browser
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        #referer url if needed
        'Referer': f'{rf_url}'
    }

    #gets response for url
    response = requests.get(url, headers=headers,stream=True)
    print(response.status_code)  # Should be 200 for OK
    print(response.headers.get('content-type')) #checks for the right content type

    
    #creates a file with the specified path and opens it as binary file as out_file    
    with open(path, 'wb') as out_file:
        #writes the image into the file in 1024 byte chunks
        for chunk in response.iter_content(1024):
            out_file.write(chunk)



#main executable when run
def main():
    service =Service()
    options=webdriver.ChromeOptions()


    #Inputs 
    folder_name=input("Enter the folder Name: ")
    url=input("Enter the url: ")
    rf_url=input("Enter if the page requires a referer url: ")
    container=input("Enter the container for the pages: ")


    #opens the Chrome web driver
    driver=webdriver.Chrome(service=service, options=options)


    #gets the save location
    save_location='Saves/'
    full_folder_path=os.path.join(save_location, folder_name)

    #if save location not found creates the directory
    if not os.path.exists(full_folder_path):
        os.makedirs(full_folder_path)

    #opens he desired url
    driver.get(url)

    #waits for the page to load
    while driver.execute_script("return document.readyState") != "complete":
        pass

    # creates a wait for 10 seconds to look for desired componenets
    wait =WebDriverWait(driver,10)

    #waits for all the images inside a particular div to load
    all_img_tags=wait.until(EC.presence_of_all_elements_located((By.XPATH,f".//div[@class='{container}']/img")))

    #creates an action chain    
    actions = ActionChains(driver)
    
    i=1 #iterable variable


    #for loop to cycle through images and save
    for image in all_img_tags:
        actions.move_to_element(image).perform() #scrolls to the current image element (for lazy loading)
        img_url=image.get_attribute('src')  #gets the source of the image
        img_extension = os.path.splitext(img_url)[1] #splits the extension of the image from the source and saves it to this variable 
        save_path=os.path.join(full_folder_path, f'00{i}{img_extension}') #creates the file path tp write to
        save_img(img_url, save_path, rf_url)#calls the save_img function defined earlier to write the image in to the file path in chunks 
        i+=1 #increment in iterable variable
        
    driver.quit()#closes driver

#run module accessibility
if __name__ == "__main__":
    while True:
        main()
