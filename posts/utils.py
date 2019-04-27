import datetime
import math
import re  # for regular expression
from django.utils.html import strip_tags

# strip_tag: Tries to remove anything that looks like an HTML tag from the
#  string, that is anything contained within <>.


def count_words(html_string):
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string)
    """Returns a list containing all matches, where the string contains
    any word characters"""
    count = len(matching_words)
    return count


def get_time_read(html_string):
    count = count_words(html_string)
    read_time_min = math.ceil(count/200.0)  # assuming 200 word per minute reading
    # read_time = str(datetime.timedelta(seconds=read_time_min))
    return int(read_time_min)  # return a string




