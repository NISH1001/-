from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# elem = driver.find_element_by_id("")
# elem.send_keys("adfa")
# elem.send_keys(Keys.RETURN)

driver = webdriver.Firefox()
driver.get("http://xnepali.net/fonts/preeti-unicode.htm")
elem = driver.find_element_by_id('legacy_text')
but = driver.find_element_by_id("converter")

b = open('engpreeti.txt', 'r')
u = open('engunicode.txt', 'w')

a = b.read().split('\n')
for x in a:
    c = x.split('>>>>')
    if len(c) ==2 :
        eng = c[0]
        pre = c[1]
        elem.clear()
        elem.send_keys(pre)
        but.send_keys(Keys.RETURN)
        soln = driver.find_element_by_id('unicode_text')
        u.write(eng+'>>>>'+soln.get_attribute('value')+'\n')

driver.close()
