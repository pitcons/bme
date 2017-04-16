import lxml.html

def body_as_etree(html):
    body = html[html.find('<body'):html.find('</body')]
    root = lxml.html.fromstring(body)
    return root
