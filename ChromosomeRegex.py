import re


def validate_regex(name):
    regex = r'^chr([1-9]|1[0-9]|2[0-2])$'
    regex = re.compile(regex)
    return regex.match(name)
