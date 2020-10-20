import scrapy
from json import dump
from tqdm import tqdm
from dosops.spiders.Utilities import is_valid_xpath, load_ids


class GcloudSpider(scrapy.Spider):
    name = "gcloud"

    def start_requests(self, ids=None):
        if not ids:
            baseurl = 'https://www.digitalmarketplace.service.gov.uk/g-cloud/services/'
            ids = load_ids(
                '/Users/catherined/Desktop/procurment_analysis/gcloud-IDs.csv', 'ID')
        for id in tqdm(ids):
            yield scrapy.Request(url=baseurl + str(id), callback=self.parse)

    def parse(self, response):
        self.logger.warning(response.url)

        entry = {}
        filename = 'gcloud-services.json'

        count_section = 1
        count_div = 1
        is_section = True
        while is_section:
            count_formatted = str(count_section).zfill(2)
            is_div = True
            try:
                is_valid_xpath(response.xpath(
                    f'//div[contains(@id,"{count_formatted}")]'))
                while is_div:
                    try:
                        fields = response.xpath(
                            f'//div[contains(@id,"{count_formatted}")]//div[{count_div}]//dt//text()')[0].root.strip()
                        fields_text = response.xpath(
                            f'//div[contains(@id,"{count_formatted}")]//div[{count_div}]//dd//text()')[0].root.strip()

                        entry[fields] = fields_text
                        self.logger.warning(
                            f'{list(entry.keys())[-1]}: {list(entry.values())[-1]}')

                        count_div += 1
                    except:
                        is_div = False
                        print(f'No div numbered {count_div}')
                count_section += 1
                count_div = 1
            except:
                is_section = False
                print(f'No Section numbered {count_formatted}')

        with open(filename, 'w') as f:
            dump(entry, f)
        self.log('Saved file %s' % filename)
