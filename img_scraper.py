from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib


from time import sleep
from random import randint

import os




def initial_call():

    url = input("Zadejte url stránky pro scraping obrázků: ")

    html_code = urlopen(url).read().decode("utf-8")

    sleep(randint(2,10))
    soup = BeautifulSoup(html_code, 'lxml')

    imges = soup.find_all("img")
    nav = soup.find("nav")
    return url, imges, nav

def get_html(urls, main_url):
    for url_pg in urls:  
        try:
            html = urlopen(main_url + "/" + url_pg.strip("/")).read().decode("utf-8")
            sleep(randint(2,10))
            soup2 = BeautifulSoup(html, 'lxml')
            imges_all = soup2.find_all("img")
            #all = soup2.find_all('a', href=True)
            return imges_all
        except:
            pass


def all_urls(href):
    url_list = []
    href = str(href).split("<a")
    for page_url in href:
        url = str(page_url).split('href="')[-1].split('"')[0]
        url_list.append(url)
    print(url_list)
    return url_list


def make_dir(url):
    to_strip = url.split(".")
    nm_file = 0
    while True:
        try:
            if "https" in url:
                dir_name = url.strip(f'https://www.{to_strip[-1]}') + str(nm_file)
                os.mkdir(dir_name)
                break
            else:
                dir_name = url.strip(f'http://www.{to_strip[-1]}') + str(nm_file)
                os.mkdir(dir_name)
                break
        except FileExistsError:
            nm_file += 1
    return dir_name


def dw_photo(img, main_url):
    dir = make_dir(main_url)
    for url_img in img:
        url_img = str(url_img).split('src="')[-1].split('"')[0]
        try:
            download = urlopen(main_url + url_img)
            img_nm = str(url_img.split("/")[-1])
            with open("./" + dir + "/" + img_nm, "wb") as f:
                f.write(download.read())
        except:
            try:
                download = urlopen(url_img)
                img_nm = str(url_img.split("/")[-1])
                with open("./" + dir + "/" + img_nm, "wb") as f:
                    f.write(download.read())
            except:
                print(url_img, " stahování tété fotky se nezdařilo")



def main():
    url, imges, nav = initial_call()
    #dw_photo(imges, url)
    dw_photo(get_html(all_urls(nav), url), url)


if __name__=="__main__":
    main()


