
from pydantic import BaseModel
from bs4 import BeautifulSoup
import re

class SingleArticle(BaseModel):
    title: str
    text: str

def cleanText(text: str) -> str:
    
    text = re.sub(r"\[\[Plik:.*?\]\]", "", text)  # remove file references from text
    text = re.sub(r"\[\[(.*)\]\]", r"\1", text)  # remove square brackets surrounding references in text
    text = re.sub(r"\{\{.*?\}\}", "", text) # remove references to other pages (usually in form of {{reference to other page}})
    text = re.sub(r" +", " ", text) # replace multiple spaces with single space

    return text

def extractPagesFromString(wiki_xml: str) -> list[SingleArticle]:
    soup = BeautifulSoup(wiki_xml, "xml")
    
    pages = soup.findChildren('page')
    articles = []
    for page in pages:
        title = page.title.text.strip()
        text = page.revision.text.strip()
        text = cleanText(text)
        articles.append(SingleArticle(title=title, text=text))
    return articles

def extractPagesFromFile(file_path: str) -> list[SingleArticle]:
    with open(file_path, "r") as file:
        wiki_xml = file.read()
    return extractPagesFromString(wiki_xml)