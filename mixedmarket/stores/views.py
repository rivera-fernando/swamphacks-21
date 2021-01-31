import os
from django.shortcuts import render
from selenium import webdriver
#from selenium import JavascriptExecutor
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from django.http import HttpResponseRedirect

from .forms import SearchForm

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("window-size=1920,1080")
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument('user-agent={0}'.format(user_agent))

# Create your views here.
def index(request):
    driver = webdriver.Chrome(options=chrome_options)
    form = SearchForm()
    clean = []

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            picked = form.cleaned_data.get('picked')
            userInput = form.cleaned_data.get('search').replace(" ", "+")
            for store in picked:
                if store == 'ae':
                    base_link = "https://www.ae.com/us/en/s/"
                    driver.get(base_link + userInput)
                    element = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.NAME, "accept-cookie"))
                    )
                    element.click()

                    num = driver.find_element_by_css_selector("span[class='search-message']")
                    real_num = int(num.text[9:num.text.index("results")])
                    while len(driver.find_elements_by_css_selector(
                            "div[class='product-tile qa-product-tile __eadf2 col-md-3 col-xs-6']")) < (
                            real_num - .07 * real_num):
                        if len(driver.find_elements_by_css_selector(
                                "div[class='product-tile qa-product-tile __eadf2 col-md-3 col-xs-6']")) > 25:
                            break
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(1)

                    results = driver.find_elements_by_css_selector(
                        "div[class='product-tile qa-product-tile __eadf2 col-md-3 col-xs-6']")
                    clean = []
                    for result in results:
                        print('going through results')
                        img = result.find_element_by_css_selector(
                            "img[class='img-responsive product-tile-image img-responsive']").get_attribute('src')
                        temp = []
                        name = result.find_element_by_css_selector("h3[class='product-name']").text
                        price = result.find_element_by_css_selector(
                            "div[class='qa-product-prices product-prices __527f1 ember-view']").text
                        link = result.find_element_by_css_selector(
                            "a[class='xm-link-to qa-xm-link-to tile-link']").get_attribute('href')
                        if "\n" in price:
                            price = price[price.index("\n") + 1:]
                        temp = [name, price, img, link, "AE"]
                        clean.append(temp)
                elif store == 'asos':
                    base_link = "https://www.asos.com/us/search/?q="
                    driver.get(base_link + userInput)
                    num = driver.find_element_by_css_selector("p[class='_2JQRAAs styleCount']")
                    real_num = int(num.text[:num.text.index("styles")].replace(",",""))

                    while len(driver.find_elements_by_css_selector("a[class='_3TqU78D']")) < (
                            real_num - .07 * real_num):
                        if len(driver.find_elements_by_css_selector("a[class='_3TqU78D']")) > 25:
                            break
                        print(len(driver.find_elements_by_css_selector("a[class='_3TqU78D']")))
                        try:
                            element = driver.find_element_by_css_selector("a[class='_39_qNys']")
                            element.click()
                        except:
                            pass
                        time.sleep(1)
                    results = driver.find_elements_by_css_selector("a[class='_3TqU78D']")
                    for result in results:
                        temp = []
                        name = result.find_element_by_css_selector("div[class='_3J74XsK']").text
                        price = result.find_element_by_css_selector("span[class='_16nzq18']").text
                        try:
                            img = result.find_element_by_css_selector(
                                "img[data-auto-id='productTileImage']").get_attribute('src')
                            temp = [name,price,img,result.get_attribute('href'), "ASOS"]
                            clean.append(temp)
                        except:
                            pass
                elif store == 'hm':
                    base_link = "https://www2.hm.com/en_us/search-results.html?q="
                    driver.get(base_link + userInput)
                    num = driver.find_element_by_css_selector("div[class='filter-pagination']")
                    real_num = int(num.text[:num.text.index("items")])

                    while len(driver.find_elements_by_css_selector("article[class='hm-product-item']")) < (
                            real_num - .07 * real_num):
                        print(len(driver.find_elements_by_css_selector("article[class='hm-product-item']")))
                        if len(driver.find_elements_by_css_selector("article[class='hm-product-item']")) > 25:
                            break
                        try:
                            element = driver.find_element_by_css_selector("button[class='button js-load-more ']")
                            element.click()
                        except:
                            pass
                        time.sleep(1)
                    results = driver.find_elements_by_css_selector("article[class='hm-product-item']")
                    for result in results:
                        temp = []
                        name = result.find_element_by_css_selector("h3[class='item-heading']").text
                        price = result.find_element_by_css_selector("span[class='price regular']").text
                        image = result.find_element_by_css_selector("img[class='item-image']").get_attribute('src')
                        if image == "":
                            image = "https:" + result.find_element_by_css_selector(
                                "img[class='item-image']").get_attribute('data-src')
                        link = result.find_element_by_css_selector(
                            "a[class='item-link remove-loading-spinner']").get_attribute('href')
                        temp = [name, price, image, link, "H&M"]
                        clean.append(temp)

            # Reset form fields
            form = SearchForm()
            driver.quit()
        else:
            print("Failure")



    args = {"form":form, 'results' : clean}
    return render(request, 'index.html', args)

def login(request):
    args ={}
    return render(request, 'login.html', args)

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')

    args={"form": form,}
    return render(request, 'register.html', args)
