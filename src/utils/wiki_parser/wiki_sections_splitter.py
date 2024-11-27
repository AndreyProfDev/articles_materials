
import re

from utils.wiki_parser.schema import ArticleSection

def split_wiki_text_by_sections(text: str) -> list[ArticleSection]:
    pattern = r"""
        ==+         # Match opening equals signs
        \s*         # Optional whitespace
        ([^=]+?)    # Section title (capture group 1)
        \s*         # Optional whitespace
        ==+        # Match closing equals signs
        \s*        # Optional whitespace
        ((?:(?!==+)[\s\S])*) # Section content (capture group 2)
    """
    
    # Find all explicit sections
    matches = list(re.finditer(pattern, text, flags=re.VERBOSE))
    sections = []

    if len(matches) == 0 and len(text.strip()) > 0:
        return [ArticleSection(title="Main", content=text.strip())]
    
    # Check for content before first section
    if matches and matches[0].start() > 0:
        main_content = text[:matches[0].start()].strip()
        sections.append(ArticleSection(title="Main", content=main_content))
    
    # Add remaining sections
    for match in matches:
        title = match.group(1).strip()
        content = match.group(2).strip()
        sections.append(ArticleSection(title=title, content=content))
    
    # If no sections found at all, treat entire text as main section
    if not sections and text.strip():
        sections.append(ArticleSection(title="Main", content=text.strip()))
        
    return sections