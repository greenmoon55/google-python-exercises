#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  match = re.search(r'_(\S+)', filename)
  if match:
    hostname = match.group(1)
  else:
    print 'hostname error'
    sys.exit(1)

  def custom_sort(url):
    match = re.search(r'-\w+-(\w+).jpg$', url)
    return match.group(1)

  file = open(filename, 'r')
  urls = re.findall(r'GET (\S+) HTTP', file.read())
  urls = [url for url in urls if re.search(r'puzzle', url)]
  if re.search(r'-\w+-\w+.jpg$', urls[0]):
    urls = sorted(set(urls), key=custom_sort) 
  else:
    urls = sorted(set(urls))
  urls = ['http://' + hostname + url for url in urls]
  return urls

  
  

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  html = """
    <html>
    <body>"""

  if not os.path.exists(dest_dir):
    os.mkdir(dest_dir)
  for index, img_url in enumerate(img_urls):
    urllib.urlretrieve(img_url, dest_dir + '/img' + str(index))
    html += '<img src="img%d">' % index
  
  html += """ 
    </body>
    </html>
  """
  file = open(dest_dir + '/index.html', 'w')
  file.write(html)
  file.close()


def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
