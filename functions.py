
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup
from nameparser import HumanName


STOPWORDS = set(stopwords.words('english'))


def format_id(text: str | int, prefix: str = '') -> str:
    return f"{prefix}{text}"


def clean_html(text: str) -> str:
    soup = BeautifulSoup(text, 'html.parser')
    clean_text = soup.get_text(' ')
    return clean_text


def format_name(text: str) -> str:
    name = HumanName(text)
    return f"{name.first} {name.last}"


def format_tags(text: str, separator=' ') -> str:
    return text.split(separator)


def remove_stopwords(text: str) -> str:
    words = word_tokenize(text)
    filtered_words = [word for word in words if word not in STOPWORDS]
    return ' '.join(filtered_words)


def extract_entities(text: str) -> str:
    # Extract entities logic
    return text


DATA_FUNCTIONS = {
    'format_id': format_id,
    'clean_html': clean_html,
    'format_name': format_name,
    'format_tags': format_tags,
    'remove_stopwords': remove_stopwords,
    'extract_entities': extract_entities,
}
