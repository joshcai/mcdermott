import urllib2
import re
from bs4 import BeautifulSoup

#majors
response = urllib2.urlopen('http://www.utdallas.edu/academics/majors.html')
html = response.read()
soup = BeautifulSoup(html, 'html.parser')

with open('majors.py', 'w') as file:
    file.write('MAJOR_CHOICES = (\n')
    for a in soup.findAll("a", { "class":"degreetitle" }):
        title = re.sub(r'([^\s\w]|_)+', '', a.getText()).strip()
        file.write('(\'' + title.upper().replace(' ', '_') + '\', \'' + a.getText().strip() + '\'),\n')
    file.write(')')
    file.close()

#minors
minor_urls = ('ah', 'bbs', 'ecs', 'epps', 'is', 'jsom', 'nsm')

with open('minors.py', 'w') as file:
    file.write('MINOR_CHOICES = (\n)')
    for url in minor_urls:
            reponse = urllib2.urlopen('catalog.utdallas.edu/now/undergraduate/programs/' + url + '/minors')
            html = reponse.read()
            soup = BeautifulSoup(html, 'html.parser')
            for a in soup.findAll("a", { "class":"external" })
    file.close()
