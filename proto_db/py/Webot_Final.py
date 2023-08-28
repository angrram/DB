from selenium import webdriver 
from selenium.webdriver.firefox.options import Options  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from progressbar import ProgressBar,Bar, Percentage
import os
import os.path
# the target website 
url = "http://www.swisstargetprediction.ch/" 
# the interface for turning on headless mode 
options = Options() 
options.set_preference("browser.download.folderList", '2')
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
options.set_preference("browser.download.folderList",2)
options.set_preference("browser.download.manager.showWhenStarting",False)
options.set_preference("browser.download.dir", os.getcwd())
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "")
options.add_argument("-headless") 
options.add_argument("--incognito")
options.add_argument('--disable-gpu') if os.name == 'nt' else None
def submit(smile,compuesto_name):
    driver = webdriver.Firefox(options=options) 
    driver.get(url) 
    com="document.forms[0].smiles.value='"
    caracter="'"
    time.sleep(5)
    try:
        driver.execute_script(com+smile+caracter)
        #print(com+smile+caracter + "\n")
    except:
        time.sleep(5)
        driver.execute_script(com+smile+caracter)
    try:
        driver.execute_script('document.getElementById("myForm").submit()')
        #print(com+smile+caracter + "\n")
    except:
        time.sleep(5)
        driver.execute_script('document.getElementById("myForm").submit()')
    dummy_boolean = False
    try:
        WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, "buttons-csv"))).click()
    except:
        print('No es posible procesarsmile: '+smile+ "\n")
    driver.close()
def cambia_nombre(ltid,compuesto_name):
    #ir a lotus/lotusid 
    #copiar el document.querySelector("#overview > div > div > div.row > div.col-sm-8 > table > tbody > tr:nth-child(1) > td:nth-child(2)")
    driver = webdriver.Firefox(options=options) 
    driver.get("https://lotus.naturalproducts.net/compound/lotus_id/"+ltid)
    path = './SwissTargetPrediction.csv'
    check_file = os.path.isfile(path)
    try:
        name_compuesto = driver.execute_script('document.querySelector("#overview > div > div > div.row > div.col-sm-8 > table > tbody > tr:nth-child(1) > td:nth-child(2)").textContent')
        os.rename("SwissTargetPrediction.csv", name_compuesto+'.csv')
    except:
        print("Permisos de usuario no suficiente para cambiar el nombre del archivo")
        #cmabiar al nombre->ltid
        if(check_file):
            try:
                os.rename("SwissTargetPrediction.csv", ltid+'.csv')        
            except:
                print("Permisos de usuario no suficiente para cambiar el nombre del archivo")
             
    
def entresacar(nombre_archivo):
    # Lista para almacenar los SMILES extraídos
    smiles_extraidos = []
    with open(nombre_archivo, 'r') as fp:
        lines = len(fp.readlines())
    pbar = ProgressBar(widgets=[Percentage(), Bar()],maxval=lines).start()
    i=0
    # Abrir el archivo en modo lectura
    with open(nombre_archivo, 'r') as archivo:
        # Leer el contenido del archivo línea por línea
        for linea in archivo:
            # Extraer los SMILES después de los primeros 11 caracteres y agregarlos a la lista
            smile = linea[11:].strip()
            ltid= linea[0:10].strip()
            #print("Copié el SMILES con exito!" + "\n")
            #print(smile)
            compuesto_name  =   ("null")
            submit(smile,compuesto_name)
            cambia_nombre(ltid,compuesto_name)
            smiles_extraidos.append(smile)
            i=i+1
            os.system('cls')
            pbar.update(i)

if __name__ == '__main__':
    nombre_archivo=".\Resultados_Bot.txt"
    entresacar(nombre_archivo)
    print("Proceso terminado con exito! :)")