import sys
import re
import argparse
import requests
import HTMLParser
from pprint import pprint
from bs4 import BeautifulSoup


def scrape(url):
    numbers = []
    r = requests.get(url)
    html = r.text
    no_script = re.sub(r"<[^>]*>", " ", html)
    emails = re.findall(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", no_script)
    phone_numbers = re.findall(r"1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?", no_script)
    links = re.findall( r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", no_script)
    for tup in phone_numbers:
        joined = "-".join(tup[:3])
        numbers.append(joined)
    
    print "emails found:\n", "\n".join(emails)
    print 
    print "phone numbers found:\n", "\n".join(numbers)
    print
    print "links found:\n", "\n".join(links)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help= 'url to pull phone numbers, emails, and links from')
    return parser

def main(args):
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(3)
    
    parsed_args = parser.parse_args(args)

    if parsed_args.url:
        return scrape(parsed_args.url)


if __name__ == '__main__':
    main(sys.argv[1:])
