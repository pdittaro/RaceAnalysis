# -*- coding: utf-8 -*-

import csv
from races.items import RaceResult
import inspect
import pdfkit
import os

from pathlib import Path


class RacesPipeline(object):
    def open_spider(self, spider):
        print("Opening File")
        self.file = open('output/races.csv', 'w', newline='')

        rr_keys = inspect.getmembers(RaceResult, lambda a: not(
            inspect.isroutine(a)))[-1][1].keys()
        self.csv_writer = csv.DictWriter(self.file, rr_keys)
        self.csv_writer.writeheader()

    def close_spider(self, spider):
        print("Closing File")
        self.file.close()

    def process_item(self, item, spider):
        item['url'] = self.normalize_url(item['url'])
        item['filename'] = self.download_pdf(item)
        self.csv_writer.writerow(item)
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

            filepath = "%s%s.pdf" % (filedir, item['race'])

            pdfkit.from_url(item['url'], filepath)
            return filepath

        else:
            return ''
