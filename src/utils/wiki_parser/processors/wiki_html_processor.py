
import html
import re


def _extract_tag_content(text: str, tag_name: str) -> str:
    pattern = rf"""
        <{tag_name}[^>]*>      # Match opening <div> with any attributes
        (?P<content>    # Named capture group for content
            (?:
                (?!<{tag_name})
                (?!</{tag_name}>)
                .
            )*?
        )
        </{tag_name}>          # Match closing </div>
    """
    return re.sub(pattern, r"\g<content>", text, flags=re.S | re.VERBOSE)

def _remove_tag_with_content(text: str, tag_name: str) -> str:
    pattern = rf"""
        <{tag_name}[^>]*>      # Match opening <div> with any attributes
        (?P<content>    # Named capture group for content
            (?:
                (?!<{tag_name})
                (?!</{tag_name}>)
                .
            )*?
        )
        </{tag_name}>          # Match closing </div>
    """
    return re.sub(pattern, "", text, flags=re.S | re.VERBOSE)

def _remove_self_closing_tags(text: str, tag_name: str) -> str:
    pattern = rf"""
        <{tag_name} 
        (?:              # Start non-capturing group
            (?!</{tag_name}>)   # Negative lookahead - don't match if next chars are </div>
            .            # Match any character
        )*?              # Repeat non-greedily
        />              # Match self-closing <div/> tag
    """
    return re.sub(pattern, "", text, flags=re.S | re.VERBOSE)

def process_wiki_html(text: str) -> str:
    
    text = text.replace("&nbsp;", " ")
    text = html.unescape(text)
    text = text.replace("<br />", "\n")
    while True:
        new_text = _extract_tag_content(text, tag_name="div")
        new_text = _extract_tag_content(new_text, tag_name="h2")
        new_text = _extract_tag_content(new_text, tag_name="span")
        new_text = _extract_tag_content(new_text, tag_name="ref")
        new_text = _remove_tag_with_content(new_text, tag_name="gallery")
        new_text = _remove_self_closing_tags(new_text, tag_name="div")
        new_text = _remove_self_closing_tags(new_text, tag_name="h2")
        new_text = _remove_self_closing_tags(new_text, tag_name="span")
        new_text = _remove_self_closing_tags(new_text, tag_name="ref")
        new_text = _remove_self_closing_tags(new_text, tag_name="gallery")
        new_text = re.sub(r" +", " ", new_text) # replace multiple spaces with single space
        new_text = re.sub(r"\n+", "\n", new_text) # replace multiple new line symbols with single new line symbol

        if new_text == text:
            text = new_text
            break
        text = new_text

    return text.strip()