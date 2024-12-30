import re
from typing import Literal

def _extract_display_text_from_piped_wikilinks(text: str) -> str:
    pattern = r"""
        \[\[            # Match opening [[
        [^\[][^\[]*     # Match any chars except [ until
        \|              # the pipe separator |
        (?P<display>    # Named capture group for display text
            [^\[][^\[]*?  # Match any chars except [ (non-greedy)
        )
        \]\]            # Match closing ]]
    """

    return re.sub(pattern, r"\g<display>", text, flags=re.S | re.VERBOSE)

def _extract_simple_wikilink_content(text: str) -> str:
    pattern = r"""
        \[\[                  # Match opening [[
        (?!                   # Negative lookahead
            :?               # Optional colon prefix
            (?:Plik|[Kk]ategoria):  # Don't match if starts with Plik: or Kategoria:/kategoria:
        )
        (?P<content>[^\[\]]*?)  # Named capture group for the content
        \]\]                  # Match closing ]]
    """
    # First pass - extract only non-category/file links
    text = re.sub(pattern, r"\g<content>", text, flags=re.S | re.VERBOSE)
    
    # Second pass - remove category/file links
    pattern_remove = r"\[\[:?(?:Plik|[Kk]ategoria):.*?\]\]"
    return re.sub(pattern_remove, "", text, flags=re.S)

def _remove_prefixed_wikilinks(text: str, link_prefix: str) -> str:
    pattern = rf"""
        \[\[                    # Match opening [[
        ({link_prefix}):      # Match either Plik: or Kategoria:
        (?:                     # Start non-capturing group
            (?!\[\[)           # Negative lookahead - don't match if next chars are [[
            .                  # Match any character
        )*?                     # Repeat non-greedily
        \]\]                    # Match closing ]]
    """
    return re.sub(pattern, "", text, flags=re.S | re.VERBOSE)

def _remove_simple_tables(text: str) -> str:
    pattern = r"""
        \{\|          # Match opening {|
        [^\{]*?      # Match any chars except { (non-greedy)
        \|\}         # Match closing |}
    """
    return re.sub(pattern, "", text, flags=re.S | re.VERBOSE)

def _remove_wiki_templates(text: str) -> str:
    pattern = r"""
        \{\{         # Match opening {{
        (?:          # Start non-capturing group
            (?!\{\{) # Negative lookahead - don't match if next chars are {{
            .        # Match any character
        )*?          # Repeat non-greedily
        \}\}         # Match closing }}
    """
    return re.sub(pattern, "", text, flags=re.S | re.VERBOSE)

def _remove_wiki_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)

def remove_http_links(text: str) -> str:
    pattern = r"""
        \[          # Opening bracket
        https?:     # http: or https:
        [^\s\]]+   # URL (non-whitespace, non-bracket chars)
        \s+        # Whitespace between URL and label
        ([^\]]+)   # Capture group for label text
        \]         # Closing bracket
    """
    text = re.sub(pattern, r"\1", text, flags=re.VERBOSE)
    
    text = re.sub(r"\[https?:[^\]]+\]", "", text)
    return text

def _extract_blockquote_content(text: str) -> str:
    pattern = r"""
        <blockquote>  # Match opening <blockquote>
        (?P<content>  # Named capture group for content
            (?:
                (?!<\/blockquote>)  # Negative lookahead
                .
            )*?
        )
        <\/blockquote>  # Match closing </blockquote>
    """
    return re.sub(pattern, r"\n\g<content>\n", text, flags=re.S | re.VERBOSE)

def _replace_list_items(text: str, list_type: Literal["numbered", "bullet"]) -> str:
    """Replace list markers with equivalent number of dashes."""
    if list_type == "numbered":
        pattern = r"\n(#+)"  # Added capture group and + quantifier
    elif list_type == "bullet":
        pattern = r"\n(\*+)"  # Added capture group and + quantifier
    else:
        raise ValueError("Invalid list type. Use 'numbered' or 'bullet'.")
    
    def replace_match(m) -> str:
        if not m or not m.group(1):
            return "\n"
        return "\n" + "-" * len(m.group(1))

    new_text = re.sub(pattern, replace_match, text, flags=re.S)
    
    # Remove empty list items
    new_text = re.sub(r"\n- *?\n", "\n", new_text, flags=re.S)
    return new_text

# def _replace_list_items(text: str) -> str:
#     new_text = re.sub(r"\n\*\*\*", "\n---", text, flags=re.S)
#     new_text = re.sub(r"\n\*\*", "\n--", new_text, flags=re.S)
#     new_text = re.sub(r"\n\*", "\n-", new_text, flags=re.S)
#     new_text = re.sub(r"\n#", "\n-", new_text, flags=re.S)
#     # new_text = re.sub(r"\n- *?\n", "\n", new_text, flags=re.S)
#     return new_text

def _remove_bold_text(text: str) -> str:
    return re.sub(r"\'\'\'", "", text)

def _remove_italic_text(text: str) -> str:
    return re.sub(r"\'\'", "", text)

def remove_wiki_control_directives(text: str) -> str:
    text = text.replace("__NOTOC__", "")
    text = text.replace("__NOEDITSECTION__", "")
    return text

def process_wiki_markdown(text: str) -> str:
    while True:
        new_text = _remove_prefixed_wikilinks(text, "Plik")
        new_text = _remove_prefixed_wikilinks(new_text, "Kategoria")
        new_text = _remove_prefixed_wikilinks(new_text, "File")
        new_text = _extract_display_text_from_piped_wikilinks(new_text)
        new_text = _extract_simple_wikilink_content(new_text)
        new_text = _remove_wiki_templates(new_text)
        new_text = _remove_wiki_comments(new_text)
        new_text = _remove_simple_tables(new_text)
        new_text = _extract_blockquote_content(new_text)
        new_text = remove_http_links(new_text)
        new_text = _replace_list_items(new_text, list_type="bullet")
        new_text = _replace_list_items(new_text, list_type="numbered")
        new_text = _remove_bold_text(new_text)
        new_text = _remove_italic_text(new_text)
        new_text = remove_wiki_control_directives(new_text)
        new_text = re.sub(r" +", " ", new_text) # replace multiple spaces with single space
        new_text = re.sub(r"\n+", "\n", new_text) # replace multiple new line symbols with single new line symbol

        if new_text == text:
            text = new_text
            break
        text = new_text

    return text.strip()