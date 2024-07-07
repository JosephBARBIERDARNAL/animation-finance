import re


def remove_unmatched_lt(text):
    """
    Remove unmatched '<' characters from text.

    Examples:

    text = '<hello world'
    remove_unmatched_lt(text)
    > 'hello world'

    text = 'hello <world>'
    remove_unmatched_lt(text)
    > 'hello <world>'
    """
    pattern = r"<(?![^<>]*>)"
    cleaned_text = re.sub(pattern, "", text)
    return cleaned_text


def count_closed_and_enclosed(text):
    """
    Count the number of closed and enclosed tags in text.

    Examples:

    text = '<hello world>'
    count_closed_and_enclosed(text)
    > 1

    text = '<hello> <world>'
    count_closed_and_enclosed(text)
    > 2
    """
    closed_pattern = r"<[^<>]*>"
    closed_tags = re.findall(closed_pattern, text)
    return len(closed_tags)
