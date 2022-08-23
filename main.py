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
    number_of_jobs = re.findall("Page \d+ of \d+ jobs", txt)[0][10:13]
    number_of_jobs = int(number_of_jobs)
    return number_of_jobs


def wget_link(q, i):
    link = 'https://au.indeed.com/jobs?q={q}&l=Australia&fromage=1&start={i}'
    command = "wget \"" + link.format(q=q, i=i) + "\" -O ->> tmp.html"
    print(command)
    os.system(command)


def get_info(q):
    number_of_jobs = get_number_of_job(q)
    number_of_page = math.ceil(number_of_jobs / 15)
    print(number_of_page)
    for n in range(1, number_of_page):
        i = str(n) + "0"
        wget_link(q, i)


def get_jobs_details():
    text = open("tmp.html", "r").read()
    soup = BeautifulSoup(text, 'html.parser')
    div_class = soup.findAll('div', class_='job_seen_beacon')
    all_jobs = []
    # for i in range(len(div_class)):

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


__getattr__("main")
