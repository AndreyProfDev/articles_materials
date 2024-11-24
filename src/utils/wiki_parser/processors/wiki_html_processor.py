
import html
import re


def _remove_div_tags(text: str) -> str:
    pattern = r"""
        <div[^>]*>      # Match opening <div> with any attributes
        (?:             # Start non-capturing group
            (?!<div)    # Negative lookahead - don't match if next chars are <div
            (?!</div>)  # Negative lookahead - don't match if next chars are </div>
            .           # Match any character
        )*?             # Repeat non-greedily
        </div>          # Match closing </div>
    """
    text = re.sub(pattern, "", text, flags=re.S | re.VERBOSE)

    pattern = r"""
        <div 
        (?:        # Start non-capturing group)
            (?!</div>)   # Negative lookahead - don't match if next chars are </div>
            .            # Match any character
        )*?              # Repeat non-greedily
        />       # Match self-closing <div/> tag
    """
    return re.sub(pattern, "", text, flags=re.S | re.VERBOSE)

def _remove_ref_tags(text: str) -> str:
    pattern = r"<ref.*?>.*?</ref>"
    text = re.sub(pattern, "", text, flags=re.S)

    pattern = r"<ref.*?/>"
    return re.sub(pattern, "", text, flags=re.S)

def process_wiki_html(text: str) -> str:
    
    text = text.replace("&nbsp;", " ")
    text = html.unescape(text)
    text = text.replace("<br />", "\n")
    while True:
        new_text = _remove_ref_tags(text)
        new_text = _remove_div_tags(new_text)
        new_text = re.sub(r" +", " ", new_text) # replace multiple spaces with single space
        new_text = re.sub(r"\n+", "\n", new_text) # replace multiple new line symbols with single new line symbol

        if new_text == text:
            text = new_text
            break
        text = new_text

    return text.strip()