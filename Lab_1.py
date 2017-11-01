import requests, re

URL = "https://www.mosigra.ru"
URL_ = URL.replace('/', '\/')
URL_ = URL_.replace('.','\.')

emails = set()
passed_urls = set()

def get_emails(url, pages = 0):
    if pages >= 10:
        return
    
    passed_urls.add(url)
    
    try:
        html = requests.get(url)
    except requests.exceptions.RequestException:
        print("Error" + url)
        return

    emails.update(re.findall(r"(?<=<a href=\"mailto:)[a-zA-Z0-9_\.\-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+", html.text))

    Absolute_url = set(re.findall(r'(?:(?<=<a href=\")'+URL_+'(?:[^\s\"]+)+)', html.text))  # все абсолютные ссылки
    Relative_url = set(re.findall(r'(?:(?<=<a href=\")\/?(?:[^\s\"]+)+)', html.text))

    #######################################################################################
    Temp = set()  # временное множество для изъятия всех не относительных ссылок
    for a in Relative_url:
        if '.' in a:
            Temp.add(a)
    Relative_url = Relative_url.difference(Temp) # Оставили только относительные ссылки

    for Rel_url in Relative_url: # Приводим все относительные ссылки к одному формату и добавляем их к множеству абсолютных ссылок
        if Rel_url[0] != '/':     
            Rel_url = '/{}'.format(Rel_url)
        Rel_url = URL + Rel_url
        Absolute_url.add(Rel_url)
    #######################################################################################
 
    for url in Absolute_url:
        if passed_urls.__contains__(url):
            continue
        get_emails(url, len(passed_urls))

get_emails(URL)
kolvo = 0
for email in emails:
    kolvo += 1
    print(email)
print('Number of emails = ', kolvo)