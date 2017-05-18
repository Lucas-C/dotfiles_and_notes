from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'


def error2str(error):
    error = str(error)
    # we remove 0x???????????? pointers so that error messages do not always differ
    try:
        i = error.index(' 0x')
        return error[:i+3] + '????????????' + error[i+15:]
    except ValueError:
        return error

def robots_txt_url(url):
    parsed = urlparse(url)
    return urljoin(parsed.scheme + '://' + parsed.netloc, 'robots.txt')

def robot_can_fetch(robots_txt_content, url):
    parser = RobotFileParser()
    parser.parse(robots_txt_content.splitlines())
    return parser.can_fetch(USER_AGENT, urlparse(url).path)
