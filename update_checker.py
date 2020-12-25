from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import hashlib
import db_commands

# This Function will return all tables listed in the website
def returnAllTables(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    table = soup.findAll('table')
    return table


# Get the links under an main notice
def getSubLinks(x, main_url):
    data = {}
    for i in range(1, len(x)):
        try:
            data[str(x[i].text)] = urljoin(main_url, str(x[i]['href']))
        except IndexError:
            print("ERROR")
    return data


# Will scrap all pages except the homepage
def getWholeData(url):
    total_data = []
    table = returnAllTables(url)
    notice = 0
    for i in range(len(table)):
        if i == 0:
            continue
        tmp = {}
        tmp['title'] = table[i].findAll("a", href=True)[0].text
        tmp['link'] = urljoin(url, table[i].findAll("a", href=True)[0]["href"])
        tmp['sublinks'] = getSubLinks(table[i].findAll("a", href=True), url)
        total_data.append(tmp)
        notice += 1
    return notice, total_data


## MD5 Hash Generator for saved html file
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


## Check If file exsists or not .. If not then create the file
def file_if_not_exsist_create(fname):
    try:
        with open(fname, "rb") as f:
            print(f"File {fname} Exsists")
            f.close()
    except FileNotFoundError as e:
        with open(fname, "w") as f:
            f.write("Tested")
            f.close()
            print(f"File {fname} Created Successfully")


def JUHomePageCheck():
    file_name = "juhomepage.html"
    file_if_not_exsist_create(file_name)
    homepage_hash = db_commands.getCurrentHashOfJUHomePage()
    r = requests.get("http://www.jaduniv.edu.in/")
    soup = BeautifulSoup(r.content, 'html5lib')
    data = str(soup.find("div", attrs={"id": "footer_menu"}))
    with open(file_name, "w") as file:
        file.write(data)
    generated_md5_hash = md5(file_name)
    if generated_md5_hash == homepage_hash:
        return homepage_hash, False
    else:
        homepage_hash = generated_md5_hash
        return homepage_hash, True


