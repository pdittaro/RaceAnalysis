# -*- coding: utf-8 -*-

import csv
from races.items import RaceResult
import inspect
import pdfkit
import os
from urllib.request import urlopen, Request

from pathlib import Path


class RacesPipeline(object):
    def open_spider(self, spider):
        print("Opening File")
        self.file = open('output/races.csv', 'w', newline='')

        rr_keys = inspect.getmembers(RaceResult, lambda a: not(
            inspect.isroutine(a)))[-1][1].keys()
        self.csv_writer = csv.DictWriter(self.file, rr_keys)
        self.csv_writer.writeheader()

        self.error_log = open('output/error.log', 'w')

    def close_spider(self, spider):
        print("Closing File")
        self.file.close()
        self.error_log.close()

    def process_item(self, item, spider):
        item['url'] = self.normalize_url(item['url'])
        item['filename'] = self.download_pdf(item)
        self.csv_writer.writerow(item)
        print("Processed: %s" % str(item))
        return item

    def normalize_url(self, url):
        base_url = "https://www.rvyc.bc.ca/RacingApps/Results/html/"
        if(url.endswith(".htm")):
            new_url = base_url + url.split("/")[-1]
            return new_url
        else:
            return url

    def download_pdf(self, item):
        if(item['url'].endswith(".htm")):

            try:
                filedir = "output/%s/%s/%s/" % (
                    item['year'], item['category'], item['series'])
            except:
                filedir = "output/%s/%s/" % (
                    item['year'], item['category'])

            try:
                os.makedirs(filedir)

            except FileExistsError:
                pass

            filepath = "%s%s" % (filedir, item['race'])
            pdfpath = filepath + ".pdf"
            htmlpath = filepath + ".html"
            options = {'quiet': ''}
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
            }

            try:
                request = Request(url=item['url'], headers=headers)
                html = urlopen(request).read()
                path = Path(htmlpath)
                with path.open(mode='wb') as f:
                    f.write(html)

            except Exception as e:
                self.error_log.write(
                    "Error fetching html: %s\n%s\n" % (str(item), e))
                filepath = 'Error'
                pass

            try:
                pdfkit.from_url(item['url'], pdfpath, options)
            except Exception as e:
                self.error_log.write(
                    "Error fetching pdf: %s\n%s\n" % (str(item), e))
                filepath = 'Error'
                pass

            return filepath

        else:
            return ''
