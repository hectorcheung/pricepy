from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import math
import pandas as pd
import glob
from datetime import datetime, timedelta, date
import re

#pip install -r requirements.txt

def panafoto():
    inicio = datetime.now()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    print(inicio)
    marcas = ['SAMSUNG', 'LG', 'SONY']
    cols = ['datos', 'precios']
    sku = pd.DataFrame(columns=cols)
    for marca in marcas:
        nums = []
        links = []
        precios = []
        datas = []
        url = 'https://www.panafoto.com/categorias/?manufacturer={}&cat1=TV%20Y%20VIDEO'.format(
            marca)
        driver_path = 'C:\chromedriver.exe'
        driver = webdriver.Chrome(
            executable_path=driver_path, options=chrome_options)
        driver.implicitly_wait(15)
        driver.get(url)
        time.sleep(10)
        text = driver.page_source
        driver.quit()
        soup = BeautifulSoup(text, "lxml")
        pages = soup.find_all('a', class_="ais-pagination--link")

        for page in pages:
            num = page.text
            if num != 'Siguiente página':
                nums.append((num))
        for i in nums:
            url2 = url + "&page=" + i
            driver = webdriver.Chrome(
                executable_path=driver_path, options=chrome_options)
            driver.implicitly_wait(15)
            driver.get(url2)
            time.sleep(6)
            text = driver.page_source
            driver.quit()
            soup = BeautifulSoup(text, "lxml")
            results = soup.find_all('a', itemprop="url")
            for result in results:
                link = result['href']
                links.append(link)

        for i in links:
            driver = webdriver.Chrome(
                executable_path=driver_path, options=chrome_options)
            driver.implicitly_wait(15)
            driver.get(i)
            time.sleep(3)
            text = driver.page_source
            driver.quit()
            soup = BeautifulSoup(text, "lxml")
            #prices = soup.find_all('span',class_="price")
            productids = soup.find_all(
                'div', class_="price-box price-final_price")
            productid = productids[0]['data-product-id']
            att = 'product-price-' + str(productid)
            prices2 = soup.find_all('span', id=att)
            att2 = "old-price-" + str(productid)
            prices3 = soup.find_all('span', id=att2)
            if len(prices3) > 0:
                offer = prices2[0]['data-price-amount']
                tag = prices3[0]['data-price-amount']
            else:
                offer = prices2[0]['data-price-amount']
                tag = prices2[0]['data-price-amount']
            precios = [offer, tag]

            infos = soup.find_all('div', class_="attribute-value")
            # for i, price in enumerate(prices, start=1):
            #precio = price.text
            # if i <=2:
            # precios.append(precio)
            for info in infos:
                data = info.text
                datas.append(data)
            to_append = [datas, precios]
            df_length = len(sku)
            sku.loc[df_length] = to_append
            datas = []
            precios = []

    sku.to_excel('sku2.xlsx', index=None)
    final = datetime.now() - inicio
    print(final)


def multimax():
    inicio = datetime.now()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    print(inicio)
    marcas = ['lg', 'samsung', 'sony', 'panasonic']
    cols = ['Desc', 'Prices']
    sku = pd.DataFrame(columns=cols)
    for marca in marcas:
        nums = ['1']
        links = []
        precios = []
        datas = []
        url = 'https://www.multimax.net/collections/vendors?q={}'.format(marca)
        driver_path = 'C:\chromedriver.exe'
        driver = webdriver.Chrome(
            executable_path=driver_path, options=chrome_options)
        driver.implicitly_wait(10)
        driver.get(url)
        time.sleep(7)
        text = driver.page_source
        driver.quit()
        soup = BeautifulSoup(text, "lxml")
        pages = soup.find_all('a', class_="text-light")

        for page in pages:
            num = page.text
            if num != 'Siguiente':
                nums.append((num))
        for i in nums:
            url2 = 'https://www.multimax.net/collections/vendors?page={}&q={}'.format(
                i, marca)
            driver = webdriver.Chrome(executable_path=driver_path)
            driver.implicitly_wait(6)
            driver.get(url2)
            time.sleep(6)
            text = driver.page_source
            driver.quit()
            soup = BeautifulSoup(text, "lxml")
            pSections = soup.find_all('div', class_="image-container")
            for pSection in pSections:
                results = pSection.find_all('a')
                for result in results:
                    if result.has_attr('href'):
                        mainPage = 'https://www.multimax.net'
                        link = result['href']
                        if link != mainPage:
                            link = mainPage + link
                            links.append(link)
        for i in links:
            driver = webdriver.Chrome(executable_path=driver_path)
            driver.implicitly_wait(3)
            driver.get(i)
            time.sleep(3)
            text = driver.page_source
            driver.quit()
            soup = BeautifulSoup(text, "lxml")
            titulo = soup.find('h1', class_='title')
            datas.append(titulo['data-default-text'])
            print(titulo['data-default-text'])
            priceSection = soup.find('div', class_="pricing lht")
            offer = priceSection.find(
                'span', class_="price sell-price font-size-14 fw-600 lht inline-block converted")
            offerPrice = offer.text

            tag = priceSection.select(
                "span.price.compare-at.text-light.font-size-14.fw-300.lht.inline-block.converted")
            if len(tag) > 0:
                tagPrice = tag[0].text
            else:
                tagPrice = offerPrice
            if tagPrice == '':
                tagPrice = offerPrice
            precios = [offerPrice, tagPrice]
            #descSection = soup.find('div',class_="description")
            #ps = descSection.find_all('p')
            to_append = [datas, precios]
            df_length = len(sku)
            sku.loc[df_length] = to_append
            datas = []
            precios = []
    sku.to_excel('mm.xlsx', index=None)
    final = datetime.now() - inicio
    print(final)

def multimax2():
    x = datetime.now()
    y = x.strftime("%Y%m%d%H%M")
    inicio = datetime.now()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    print(inicio)
    productos = ['televisores','celulares','monitores','aires-acondicionados','estufas','refrigeradoras','lavadoras','secadoras','audifonos/inalámbricos','audio']
    brands =['LG','Samsung','Sony','Panasonic','HP','Beko','Mabe','Whirlpool']
    cols = ['Desc', 'Prices']
    cols2 = ['Brand','Link','Precios','Model']
    sku = pd.DataFrame(columns=cols)
    df_link = pd.DataFrame(columns=cols2)
    for producto in productos:
        nums = ['1']
        links = []
        datas = []
        url = 'https://www.multimax.net/collections/{}'.format(producto)
        driver_path = 'D:\chromedriver.exe'
        driver = webdriver.Chrome(
            executable_path=driver_path, options=chrome_options)
        driver.implicitly_wait(6)
        driver.get(url)
        time.sleep(7)
        text = driver.page_source
        driver.quit()
        soup = BeautifulSoup(text, "lxml")
        pages = soup.find_all('a', class_="text-light")

        for page in pages:
            num = page.text
            if (num != 'Siguiente' ) & (num!= '1'):
                nums.append((num))
        for i in nums:
            url2 = 'https://www.multimax.net/collections/{}?page={}'.format(
                producto, i)
            driver = webdriver.Chrome(executable_path=driver_path)
            driver.implicitly_wait(1)
            driver.get(url2)
            time.sleep(1)
            text = driver.page_source
            driver.quit()
            soup = BeautifulSoup(text, "lxml")
            articulos = soup.find_all('article')
            x = 0
            for articulo in articulos:
                precios =[]
                campo_marca = articulo.select("div.vendor.lht.font-size-14")
                marca = campo_marca[0].select('a[href]')
                campo_precio = articulo.select("div.pricing.lht")
                los_precios = campo_precio[0].select('span')
                for item in los_precios:
                    try:
                        precios.append(item.text)
                    except:
                        precios.append('NA')
                                   

                if marca[0]['title'] in brands:
                    link = articulo.select("a")[0]['href']
                    link = 'https://www.multimax.net'+link
                    driver = webdriver.Chrome(executable_path=driver_path)
                    driver.implicitly_wait(1)
                    driver.get(link)
                    time.sleep(1)
                    text = driver.page_source
                    driver.quit()
                    soup = BeautifulSoup(text, "lxml")
                    cod ='NA'
                    try:
                        upc = soup.select("div.description")[0]
                        cods = upc.find_all("p")
                        for item in cods:
                            texto = item.text
                            if 'Cod' in texto:
                                cod = texto
                                try:
                                    cod = cod.split('Cod. ')[1]
                                except:
                                    cod = cod
                                break
                    except:
                        cod ='NA'
                    to_append2 = [marca[0]['title'], link,precios,cod]
                    print(marca[0]['title'], cod,precios)
                    df_length2 = len(df_link)
                    df_link.loc[df_length2] = to_append2
    df_link.to_excel('mmsku {}.xlsx'.format(y),index=None)
    final = datetime.now() - inicio
    print(final)



def photura():
    inicio = datetime.now()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    print(inicio)
    marcas = ['LG', 'Samsung', 'Sony']
    cols = ['Desc', 'Prices']
    sku = pd.DataFrame(columns=cols)
    for marca in marcas:
        nums = ['1']
        links = []
        precios = []
        datas = []
        url = 'https://www.photura.com/collections/televisores/marca_{}'.format(
            marca)
        driver_path = 'C:\chromedriver.exe'
        driver = webdriver.Chrome(
            executable_path=driver_path, options=chrome_options)
        driver.implicitly_wait(10)
        driver.get(url)
        time.sleep(10)
        text = driver.page_source
        driver.quit()
        soup = BeautifulSoup(text, "lxml")
        pages = soup.find_all('a', class_="text-light")

        for page in pages:
            num = page.text
            if num != 'Siguiente':
                nums.append((num))
        for i in nums:
            url2 = 'https://www.multimax.net/collections/vendors?page={}&q={}'.format(
                i, marca)
            driver = webdriver.Chrome(executable_path=driver_path)
            driver.implicitly_wait(6)
            driver.get(url2)
            time.sleep(6)
            text = driver.page_source
            driver.quit()
            soup = BeautifulSoup(text, "lxml")
            pSections = soup.find_all('div', class_="image-container")
            for pSection in pSections:
                results = pSection.find_all('a')
                for result in results:
                    if result.has_attr('href'):
                        mainPage = 'https://www.multimax.net'
                        link = result['href']
                        if link != mainPage:
                            link = mainPage + link
                            links.append(link)
        for i in links:
            driver = webdriver.Chrome(executable_path=driver_path)
            driver.implicitly_wait(3)
            driver.get(i)
            time.sleep(3)
            text = driver.page_source
            driver.quit()
            soup = BeautifulSoup(text, "lxml")
            titulo = soup.find('h1', class_='title')
            datas.append(titulo['data-default-text'])
            print(titulo['data-default-text'])
            priceSection = soup.find('div', class_="pricing lht")
            offer = priceSection.find(
                'span', class_="price sell-price font-size-14 fw-600 lht inline-block converted")
            offerPrice = offer.text

            tag = priceSection.select(
                "span.price.compare-at.text-light.font-size-14.fw-300.lht.inline-block.converted")
            if len(tag) > 0:
                tagPrice = tag[0].text
            else:
                tagPrice = offerPrice
            if tagPrice == '':
                tagPrice = offerPrice
            precios = [offerPrice, tagPrice]
            #descSection = soup.find('div',class_="description")
            #ps = descSection.find_all('p')
            to_append = [datas, precios]
            df_length = len(sku)
            sku.loc[df_length] = to_append
            datas = []
            precios = []
    sku.to_excel('mm.xlsx', index=None)
    final = datetime.now() - inicio
    print(final)


def panafoto2():
    inicio = datetime.now()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    print(inicio)
    datos = []
    marcas = ['lg', 'samsung', 'sony', 'panasonic']
    cats = ['TV%20Y%20VIDEO','AUDIO','HOGAR','CELLARES%20Y%20TABLETS','CÓMPUTO']
    cat3 = "SMARTPHONES"
    cols = ['# cat', 'datos', 'precios']
    sku = pd.DataFrame(columns=cols)
    cols2 = ['url', 'link']
    df_link = pd.DataFrame(columns=cols2)
    for marca in marcas:
        nums = []
        links = []
        precios = []
        datas = []
        paginas = []
        for cat in cats:
            if (marca == "sony" and (cat != "TV%20Y%20VIDEO" or cat != "AUDIO")) or (marca == "panasonic" and cat != "HOGAR") or (marca=="lg") or (marca=="samsung"):
                url = 'https://www.panafoto.com/categorias/marcas/{}/?cat1={}'.format(marca,cat)
                if cat == "CELLARES%20Y%20TABLETS":
                    url = 'https://www.panafoto.com/categorias/marcas/{}/?cat1={}&cat3={}'.format(marca,cat,cat3)
                if marca == "panasonic":
                    url = 'https://www.panafoto.com/categorias/marcas/{}/?cat1={}&cat3=AIRES%20ACONDICIONADOS%20SPLIT'.format(marca,cat)
                print(marca, cat)
                driver_path = 'C:\chromedriver.exe'
                driver = webdriver.Chrome(
                    executable_path=driver_path, options=chrome_options)
                driver.implicitly_wait(15)
                driver.get(url)
                time.sleep(7)
                text = driver.page_source
                driver.quit()
                soup = BeautifulSoup(text, "lxml")
                pages = soup.select('span[itemprop="numberOfItems"]')
                print(pages)
                num = pages[0].text
                print(num)
                x = math.ceil(int(num)/9)

                for i in range(x):
                    j = i + 1
                    url2 = url + "&page=" + str(j)
                    paginas.append(url2)
                for pagina in paginas:
                    driver = webdriver.Chrome(
                        executable_path=driver_path, options=chrome_options)
                    driver.implicitly_wait(15)
                    print("Estamos en la " + pagina)
                    driver.get(pagina)
                    time.sleep(6)
                    text = driver.page_source
                    driver.quit()
                    soup = BeautifulSoup(text, "lxml")
                    results = soup.find_all('a', itemprop="url")
                    for result in results:
                        link = result['href']
                        links.append(link)
                        to_append2 = [pagina, link]
                        df_length2 = len(df_link)
                        df_link.loc[df_length2] = to_append2

                for i in links:
                    print("Estamos en la " + i)
                    driver = webdriver.Chrome(
                        executable_path=driver_path, options=chrome_options)
                    driver.implicitly_wait(15)
                    driver.get(i)
                    time.sleep(3)
                    text = driver.page_source
                    driver.quit()
                    soup = BeautifulSoup(text, "lxml")
                    #prices = soup.find_all('span',class_="price")
                    #productids = soup.find_all('div',class_="price-box price-final_price")
                    productids = soup.select("div.price-box.price-final_price")
                    try:
                        productid = productids[0]['data-product-id']
                        print(productid)
                        att = 'product-price-' + str(productid)
                        prices2 = soup.find_all('span', id=att)
                        att2 = "old-price-" + str(productid)
                        prices3 = soup.find_all('span', id=att2)
                        if len(prices3) > 0:
                            offer = prices2[0]['data-price-amount']
                            tag = prices3[0]['data-price-amount']
                        else:
                            offer = prices2[0]['data-price-amount']
                            tag = prices2[0]['data-price-amount']
                        precios = [offer, tag]

                        infos = soup.find_all('div', class_="attribute-value")
                        # for i, price in enumerate(prices, start=1):
                        #precio = price.text
                        # if i <=2:
                        # precios.append(precio)
                        for info in infos:
                            data = info.text
                            datas.append(data)
                        data_list = ','.join(datas)
                        price_list = ','.join(precios)
                        categorias = len(datas)
                        to_append = [categorias, data_list, price_list]
                        df_length = len(sku)
                        print(to_append)
                        sku.loc[df_length] = to_append
                        sku.to_excel('sku pf preview.xlsx', index=None)
                        datas = []
                        precios = []
                    except Exception as e: 
                        print(e)
                        print("skipped {}".format(i))
            
    x = datetime.now()
    y = x.strftime("%Y%m%d%H%M")
    df_link.to_excel('pf_link.xlsx', index=None)
    sku.to_excel('sku {}.xlsx'.format(y), index=None)
    df = sku
    maxNum = 7
    maxInDf = df['# cat'].max()
    if maxInDf < maxNum:
        maxNum = maxInDf
    for i in range(maxNum):
        col = 'cat_' + str(i + 1)
        df[col] = df['datos'].str.split(',').str[i]
    df['Tag'] = df['precios'].str.split(',').str[1]
    df['Offer'] = df['precios'].str.split(',').str[0]
    df = df.astype({'Tag': 'float'})
    df = df.astype({'Offer': 'float'})
    df = df.drop(columns=['datos', 'precios'])
    df_mapp = pd.read_excel('model_master_osd.xlsx')
    df = pd.merge(df, df_mapp, on='cat_2', how='left')
    df = df[df['PG1'] != 'No Aplica']
    df.sort_values(by=['PG1', 'PG2', 'Offer'], ascending=[
                   True, True, False], inplace=True)
    df.to_excel('panafoto_sku {}.xlsx'.format(y), index=None)
    df.to_json('pf.json', orient='records')
    final = datetime.now() - inicio
    print(final)


panafoto2()
#multimax2()

def panafile():
    df = pd.read_excel('sku 202009281114.xlsx')
    maxNum = 7
    maxInDf = df['# cat'].max()
    if maxInDf < maxNum:
        maxNum = maxInDf
    for i in range(maxNum):
        col = 'cat_' + str(i + 1)
        df[col] = df['datos'].str.split(',').str[i]
    df['Tag'] = df['precios'].str.split(',').str[1]
    df['Offer'] = df['precios'].str.split(',').str[0]
    df = df.astype({'Tag': 'float'})
    df = df.astype({'Offer': 'float'})
    df = df.drop(columns=['datos', 'precios'])
    df_mapp = pd.read_excel('model_master_osd.xlsx')
    df = pd.merge(df, df_mapp, on='cat_2', how='left')
    df = df[df['PG1'] != 'No Aplica']
    df.sort_values(by=['PG1', 'PG2', 'Offer'], ascending=[
                   True, True, False], inplace=True)
    df.to_excel('panafoto_sku4.xlsx', index=None)
    df.to_json('pf3.json', orient='index')
    df.to_json('pf2.json', orient='records')


# panafile()

def consolidar():
    inicio = datetime.now()
    path = r'D:/Python/Reportes/sku/'  # use your path
    all_files = glob.glob(path + "*.xlsx")
    print(all_files)
    li = []
    for filename in all_files:
        print(filename)
        df = pd.read_excel(filename, index_col=None, header=0)
        df['Date'] = filename.split(' ')[1].split('.')[0]
        df['Week'] = date(int(filename.split(' ')[1][:4]), int(
            filename.split(' ')[1][4:6]), int(filename.split(' ')[1][6:8])).isocalendar()[1]
        li.append(df)

    df1 = pd.concat(li, axis=0, ignore_index=True)
    df1 = df1.fillna(0)
    df = df1
    maxNum = 7
    maxInDf = df['# cat'].max()
    if maxInDf < maxNum:
        maxNum = maxInDf
    for i in range(maxNum):
        col = 'cat_' + str(i + 1)
        df[col] = df['datos'].str.split(',').str[i]
    df['Tag'] = df['precios'].str.split(',').str[1]
    df['Offer'] = df['precios'].str.split(',').str[0]
    df = df.astype({'Tag': 'float'})
    df = df.astype({'Offer': 'float'})
    df = df.drop(columns=['datos', 'precios'])
    df_mapp = pd.read_excel('model_master_osd.xlsx')
    df = pd.merge(df, df_mapp, on='cat_2', how='left')
    df = df[df['PG1'] != 'No Aplica']
    df.sort_values(by=['PG1', 'PG2', 'Offer'], ascending=[
                   True, True, False], inplace=True)
    df.to_json('pf.json', orient='records')
    df.to_excel('pf_consolidado.xlsx',index=None)
    final = datetime.now() - inicio
    print(final)


def ata():
    df = pd.read_excel('ata template.xlsx', dtype={
                       'TAG LG': str, 'PROMO LG': str, 'TAG COMP': str, 'PROMO LG': str})
    df = df.fillna('')
    html = df.to_html()
    df.to_json('ata.json', orient='records')
    print(html)

# ata()

def clientes():
    df = pd.read_excel('clientes.xlsx')
    df.to_json('clientes.json', orient='records')
clientes()

#consolidar()
#filename = r'D:/Python/Reportes/sku/sku 202009111230.xlsx'

#print(filename.split(' ')[1][6:8])

def wtf():
    mm = 'mmlinks.xlsx'
    df = pd.read_excel(mm)
    df['Model'] = 'Model'
    lr = len(df)
    for r in range(lr):
        marca = df.at[r,'Brand']
        marca = marca.lower()
        modelo = df.at[r,'Link'].split(marca+"-")[1]
        modelo = modelo.split('-')[0]
        df.at[r,'Model'] = modelo
    df.to_excel('mmsku.xlsx',index=None)
