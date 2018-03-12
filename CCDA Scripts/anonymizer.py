from bs4 import BeautifulSoup
import io

xml = open("./ccda.xml", "r")

parsedXML = BeautifulSoup(xml, "lxml")

print(parsedXML.prettify())