import csv
import os
import re
import math
from bs4 import BeautifulSoup
import argparse


def get_number_of_job(param):
    link = 'https://au.indeed.com/jobs?q={q}&l=Australia&fromage=1&start={i}'
    command = "wget \"" + link.format(q=param, i="0") + "\" -O tmp.html"
    print(command)
    os.system(command)
    f = open("tmp.html", "r")
    txt = f.read()
    text = open("tmp.html", "r").read()
    soup = BeautifulSoup(text, 'html.parser')
    #If 14 days 
    # number_of_jobs= soup.find("div",id="searchCountPages").text.replace(',', '')[31:36]
    # number_of_jobs=int(number_of_jobs)
    # print(number_of_jobs)
    number_of_jobs = re.findall("Page \d+ of \d+ jobs", txt)[0][10:14]
    number_of_jobs = int(number_of_jobs)
    return number_of_jobs

def wget_link(link):
    command = "wget \"" + link + "\" -O ->> link.html"
    os.system(command)

def wget_job(q, i):
    link = 'https://au.indeed.com/jobs?q={q}&l=Australia&fromage=1&start={i}'
    command = "wget \"" + link.format(q=q, i=i) + "\" -O ->> tmp.html"
    print(command)
    os.system(command)

def get_description(link):
    wget_link(link)
    text = open("link.html", "r").read()
    soup = BeautifulSoup(text, 'html.parser')
    job_class = soup.find('div', class_="jobsearch-jobDescriptionText")
    des=str(job_class).replace('<div class="jobsearch-jobDescriptionText" id="jobDescriptionText"><div></div>','').replace('<div>\n','').replace('</div>\n','').replace('</div>','').replace('<b>','').replace('</b>','').replace('<li>','').replace('</ul>','').replace('<ul>','').replace('<br/>','').replace('<i>','').replace('</i>','').replace('<p>','').replace('</p>','')
    return des


def get_info(q):
    number_of_jobs = get_number_of_job(q)
    number_of_page = math.ceil(number_of_jobs / 15)
    print(number_of_page)
    for n in range(1, number_of_page):
        i = str(n) + "0"
        wget_job(q, i)


def get_jobs_details():
    text = open("tmp.html", "r").read()
    soup = BeautifulSoup(text, 'html.parser')
    div_class = soup.findAll('div', class_='job_seen_beacon')
    all_jobs = []

    for i in range(len(div_class)):
        job = []
        link = "https://indeed.com.au" + div_class[i].a['href']  # link
        hyper_link = '=HYPERLINK("' + link + '")'
        position = getattr(div_class[i].a.span, 'text', None)  # position
        company_name = getattr(div_class[i].find("a", class_="turnstileLink companyOverviewLink"), 'text',
                               None)  # company name
        company_rate = getattr(div_class[i].find("span", class_="ratingsDisplay withRatingLink"), 'text',
                               None)  # company rate
        location = getattr(div_class[i].find("div", class_="companyLocation"), 'text', None)  # location
        attribute = getattr(div_class[i].find("div", class_="attribute_snippet"), 'text', None)
        #description = get_description(link) # too long, too much requests, if use add to var bellow

        var = [hyper_link, position, company_name, company_rate, location, attribute]
        for v in var:
            job.append(v)
        all_jobs.append(job)
        to_csv(job)

    return all_jobs


def to_csv(arr):
    a = []
    a.append(arr)
    with open('myfile.csv', 'a', newline='') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerows(a)


def __getattr__(name):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-q", "--quest", default="IT", help="Insert quest")
    args = vars(parser.parse_args())
    q = args["quest"]
    get_info(q)
    os.system("rm myfile.csv")
    get_jobs_details()
    #get_description("https://au.indeed.com/viewjob?jk=f8e4ea49037e1d9b&tk=1gb5l2cjois5p800&from=serp&vjs=3&advn=742642328266002&adid=395532684&ad=-6NYlbfkN0BJG9y3HqDq1UrsL1yS36eji4Wa8aOTFkGDtV0UVAvQv8Gdx7nNMHGXRAyTqhu1XLDlBJYrCkkOV8fPU82QzXEb_Q6KgnB9-YRZIoTsavliWxBAKi9jImlbQCXYfGJdS4Qt50Vmb4y8eCvI41d1CLaUNXfhwpKLwRr415xeLmkUB_EDcgJclgljOs0izs0lySqXipIAmO4Lm6GCGyAcqgs9QGJ9leQCRoLnGxlvtYXSksfC3zuRPXXS8FAFzPyYB007GWdyFslKu2tsIISwkc6CKRLBX7Wm5iHEDaw-lVX4Jr1r_FxBqMMN2-Cjaa8hQSWSYUzT_99X9YgWGkKnh_U9sCcePSJx-ztAqkj6mFdBIw==&sjdu=ab_jN-s1IW_zU0BCrfb3pAzVVmVAdOxpI_gK6Pwy05Agr_S1W0bu4l5SKlyKdzTtGkiL_Jk6eJHPQrhyhA20lQDPqshxPTWNQbr3De1CgQcZOa_1EGtEkjRa3Rc19he8LvlCM4M6p-1EygJQHRDBExsgrtEadDJeYNkAPZy7YB8uffaP4rCb3sX21CRmcWn8OdDpNO5_DvWFJazXaLuHCOnkWflLdO-AbgaWEh-5eKp7XxPX6gxwg0Hngh37ssTU_3yQYE32Z0Has1eSmOAfOjQ2b9Il319ZICwwVIqdchs")


__getattr__("main")
