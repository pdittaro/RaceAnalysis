# -*- coding: utf-8 -*-
import scrapy


class RaceResultsSpider(scrapy.Spider):
    name = 'race_results'
    allowed_domains = ['rvyc.bc.ca']

    def start_requests(self):
        urls = [
            # 'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2019',
            # 'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2018',
            # 'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2017',
            # 'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2015-2016',
            # 'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2014-2015',
            # 'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2013-2014',
            # 'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2012-2013',
            # 'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2011-2012',
            # 'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2010-2011',
            # Start of individual races in series 'R0X'
            # 'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2009-2010',
            # 'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2008-2009',
            # 'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2007-2008',
            # 'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2006-2007',
            # 'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2005-2006',
            # 'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2004-2005',
            # 'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2003-2004',
            'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2002-2003',
            # 'https://www.rvyc.bc.ca/RacingApps/Results/rr.php?content=Racing_Results.php&season=2001-2002'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        year = response.url.split("=")[-1]

        races = response.xpath(
            '//a[@target="blank" and not(@color) and not(@style)]'
        )
        print("Year:   ", year)
        print("Number of races: ", len(races))
        print("---")
        for race in races:
            series = race.xpath(
                './preceding::*[@class="event_header" or text()="Trophy Races"]/text()')[-1:].get()
            print("Series: ", series)
            title = race.xpath('./text()').get()
            print("Title:  ", title)

        pass
