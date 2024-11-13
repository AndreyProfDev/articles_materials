
from pydantic import BaseModel
from bs4 import BeautifulSoup
import re

class SingleArticle(BaseModel):
    title: str
    text: str

def cleanText(text: str) -> str:
    
    while True:
        new_text = re.sub(r"\[\[Plik:[^\[][^\[]*?\]\]", "", text, flags=re.S)  # remove file references from text
        new_text = re.sub(r"\[\[Kategoria:[^\[][^\[]*?\]\]", "", new_text, flags=re.S)  # remove category references from text
        new_text = re.sub(r"\[\[[^\[][^\[]*\|([^\[][^\[]*?)\]\]", r"\1", new_text, flags=re.S)  # remove square brackets surrounding references in text
        new_text = re.sub(r"\[\[([^\[][^\[]*?)\]\]", r"\1", new_text, flags=re.S)  # remove square brackets surrounding references in text
        new_text = re.sub(r"\{\{.*?\}\}", "", new_text, flags=re.S) # remove references to other pages (usually in form of {{reference to \nother page}})
        new_text = re.sub(r"<ref>.*?</ref>", "", new_text, flags=re.S) # remove references to other pages
        new_text = re.sub(r"\{\|[^\{][^\|]*?\|\}", "", new_text, flags=re.S) # remove tables
        new_text = re.sub(r" +", " ", new_text) # replace multiple spaces with single space
        new_text = re.sub(r"\n+", "\n", new_text) # replace multiple new line symbols with single new line symbol
        new_text = re.sub(r"\n\*", "\n", new_text, flags=re.S) # remove bullet points
        new_text = re.sub(r"\'\'\'", "", new_text) # remove bold text markdown
        new_text = re.sub(r"\'\'", "", new_text) # remove italic text markdown

        if new_text == text:
            text = new_text
            break
        text = new_text

    return text.strip()

def extractPagesFromString(wiki_xml: str) -> list[SingleArticle]:
    soup = BeautifulSoup(wiki_xml, "xml")
    
    pages = soup.findChildren('page')
    articles = []
    for page in pages:
        title = page.title.text.strip()
        text = page.revision.findChild('text').text.strip()
        text = cleanText(text)
        
        if len(text) > 0:
            articles.append(SingleArticle(title=title, text=text))
    return articles

def extractPagesFromFile(file_path: str) -> list[SingleArticle]:
    with open(file_path, "r") as file:
        wiki_xml = file.read()
    return extractPagesFromString(wiki_xml)