import scrapy
from json import dump
#from Utilities import isValidXpath


class GcloudSpider(scrapy.Spider):
    name = "gcloud"

    def start_requests(self):
        baseurl = 'https://www.digitalmarketplace.service.gov.uk/g-cloud/services/624695628011497'
        yield scrapy.Request(url=baseurl, callback=self.parse)

    def parse(self, response):
        self.logger.warning(response.url)

        entry = {}
        filename = 'gcloud-services.json'

        countSection = 1
        countDiv = 1
        is_section = True
        while is_section:
            count_formatted = str(countSection).zfill(2)
            is_div = True
            try:
                # isValidXpath(response.xpath(
                #  f'//div[contains(@id,"{count_formatted}")]'))
                while is_div:
                    try:
                        fields = response.xpath(
                            f'//div[contains(@id,"{count_formatted}")]//div[{countDiv}]//dt//text()')[0].root.strip()
                        fields_text = response.xpath(
                            f'//div[contains(@id,"{count_formatted}")]//div[{countDiv}]//dd//text()')[0].root.strip()

                        entry[fields] = fields_text
                        self.logger.warning(
                            f'{list(entry.keys())[-1]}: {list(entry.values())[-1]}')

                        countDiv += 1
                    except:
                        is_div = False
                        print(f'No div numbered {countDiv}')
                countSection += 1
                countDiv = 1
            except:
                is_section = False
                print(f'No Section numbered {count_formatted}')

        with open(filename, 'w') as f:
            dump(entry, f)
        self.log('Saved file %s' % filename)
