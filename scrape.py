import sys
import re
import argparse
import requests
import urllib2
import HTMLParser
from pprint import pprint
from bs4 import BeautifulSoup


def scrape(url):
    numbers = []
    r = requests.get(url)
    html = r.text
    links = []
    imgs = []
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, features="html.parser")
    soup.prettify()
    for anchor in soup.findAll('a', href=True):
         links.append(anchor['href'])
    href_links = [str(r) for r in links]
    for image in soup.findAll('img', src=True):
        imgs.append(image['src']) 

    no_script = re.sub(r"<[^>]*>", " ", html)
    phone_numbers = re.findall(r"1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})\W*([0-9]{4})(\se?x?t?(\d*))?", no_script)
    emails = re.findall(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", no_script)
    for tup in phone_numbers:
         joined = "-".join(tup[:3])
         numbers.append(joined)

    print "---- phone numbers found: \n", "\n".join(list(set(numbers)))
    print
    print "----emails found:\n", "\n".join(list(set(emails)))
    print
    print "----links found: \n {}".format("\n".join(list(set(href_links))))
    print
    print "----images found: \n {}".format("\n".join(list(set(imgs))))
  
    





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
