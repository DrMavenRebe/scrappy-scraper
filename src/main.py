#!/usr/bin/python2.7
#
# Copyright (C) 2012 Canaryware Inc.

__author__ = ('David Bremner <david@canaryware.com>')

import csv
import scrapemark
import time

class Scraper():
  """
      A collection of HTML scrapers. Use to pull trending links and best test 
      social APIs. 
  """

  # Grab the top 20 links from Digg's home page.
  def scrape_digg(self):
    urls = scrapemark.scrape("""
          <body>
            <div class='stories-container'>
              {*
                <div class="story-domain">
                  <a class="story-link" href='{{ [links] }}'></a>
                </div>
              *}
            </div>
          </body>
        """,
        url='http://digg.com/')['links']
    return urls

  # Grab 10 pages from the Topsy 100 list.
  def scrape_topsy(self):
    urls = scrapemark.scrape("""
          <body>
            <div class="list">
              {*
                  <h3 class="title">
                  <a href='{{ [links].url }}'></a>
                  </h3>
              *}
            </div>
          </body>
        """,
        url='http://topsy.com/top100')['links']

    for page, offset in enumerate([15,30,45,60,75,90,105,120,135]):
      urls += scrapemark.scrape("""
          <body>
            <div class="list">
              {*
                  <h3 class="title">
                  <a href='{{ [links].url }}'></a>
                  </h3>
              *}
            </div>
          </body>
        """,
        url='http://topsy.com/top100?offset='+str(offset)+'&om=f&page='+str(page+1)+'&thresh=top100')['links']

    return urls
  
  # Grab a total of 60 of the top most emailed, most bloged and viewed on the New York Times.
  def scrape_nyt(self):
    urls = scrapemark.scrape("""
          <body>    
              {*
                <div class='element2'>
                  <h3> <a href='{{ [links].url }}'></a> </h3>
                </div>
              *}
          </body>
        """,
        url='http://www.nytimes.com/most-popular-emailed')['links']

    urls += scrapemark.scrape("""
          <body>    
              {*
                <div class='element2'>
                  <h3> <a href='{{ [links] }}'></a> </h3>
                </div>
              *}
          </body>
        """,
        url='http://www.nytimes.com/most-popular-viewed')['links']

    urls += scrapemark.scrape("""
          <body>    
              {*
                <div class='element2'>
                  <h3> <a href='{{ [links] }}'></a> </h3>
                </div>
              *}
          </body>
        """,
        url='http://www.nytimes.com/most-popular-blogged')['links']

    return urls

  # Write a scrapped file disk as a CSV.
  def write_to_file(self, rows, filePath='../../data/'):
    fileName = filePath + str(int(time.time())) + '.csv'
    f = open(fileName, 'wb')
    for row in rows:
      f.write(str(row) + ',\n')

  # Run all the scrapers and all the data to file accordingly.
  # save: if True, save the files to disc respectfully.
  # return the list
  def scrape_all(self, save=True):
    digg = self.scrape_digg()
    print 'Found', len(digg), 'Digg items to file.'

    topsy = self.scrape_topsy()
    print 'Found', len(topsy), 'Topsy items to file.'

    nyt = self.scrape_nyt()
    print 'Found', len(nyt), 'New York Times items to file.'

    if save:
      self.write_to_file(digg, filePath='../data/scrapped/digg/')
      self.write_to_file(topsy, filePath='../data/scrapped/topsy/')
      self.write_to_file(nyt, filePath='../data/scrapped/nyt/')

    return digg + topsy + nyt

if __name__ == '__main__':
  s = Scraper()
  s.scrape_all()
