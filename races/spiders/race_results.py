# -*- coding: utf-8 -*-
import scrapy
from races.items import RaceResult


class RaceResultsSpider(scrapy.Spider):
    name = 'race_results'
    allowed_domains = ['rvyc.bc.ca']

    def start_requests(self):
        urls = [
            'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2019',
            'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2018',
            'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2017',
            'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2015-2016',
            'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2014-2015',
            'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2013-2014',
            'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2012-2013',
            'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2011-2012',
            'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2010-2011',
            # Start of individual races in series 'R0X'
            'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2009-2010',
            'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2008-2009',
            'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2007-2008',
            'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2006-2007',
            'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2005-2006',
            'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2004-2005',
            'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2003-2004',
            'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2002-2003',
            'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2001-2002'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        year = response.url.split("=")[-1]

        # Get series races
        series = response.xpath(
            '//*[@class="racing_results1"]'
        )

        for s in series:
            if (len(s.xpath('./a').extract()) == 0):
                break

            first_element = s.xpath('./a[1]')
            if(first_element.extract_first()):
                x = first_element.xpath('text()').get().split('\xa0')
                series = x[0]

                first_title = x[1]
                first_href = first_element.xpath('@href').get()

                category = first_element.xpath(
                    './preceding::*[@class="event_header" or text()="Trophy Races"]/text()')[-1:].get()

                rr = RaceResult()
                rr['year'] = year
                rr['category'] = category
                rr['series'] = series
                rr['race'] = first_title
                rr['url'] = first_href
                yield rr

                results = s.xpath('./a[position()>1]')
                for result in results:
                    title = result.xpath('text()').get()
                    url = result.xpath('@href').get()

                    rr = RaceResult()
                    rr['year'] = year
                    rr['category'] = category
                    rr['series'] = series
                    rr['race'] = title
                    rr['url'] = url
                    yield rr

            else:
                print("ERROR in %s" % year)

        # Trophy Races and Mini 12 / 2.4m

        races = response.xpath(
            '//*[not(self::div)]/a[@target="blank"]'
        )

        for race in races:

            category = race.xpath(
                './preceding::*[@class="event_header" or text()="Trophy Races"]/text()')[-1:].get()
            title = race.xpath('text()').get()
            url = race.xpath('@href').get()

            rr = RaceResult()
            rr['year'] = year
            rr['category'] = category
            rr['race'] = title
            rr['url'] = url
            yield rr

        pass
