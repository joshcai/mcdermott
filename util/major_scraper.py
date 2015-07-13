import urllib2
import re
from bs4 import BeautifulSoup

response = urllib2.urlopen('http://www.utdallas.edu/academics/majors.html')
html = response.read()
soup = BeautifulSoup(html, 'html.parser')

with open('majors.py', 'w') as file:
    file.write('MAJOR_CHOICES = (\n')
    for a in soup.findAll("a", { "class":"degreetitle" }):
        title = re.sub(r'([^\s\w]|_)+', '', a.getText()).strip()
        file.write('(' + title.upper().replace(' ', '_') + ', \'' + a.getText().strip() + '\'),\n')
    file.write(')')
    file.close()
