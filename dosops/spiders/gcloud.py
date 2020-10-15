import scrapy


class GcloudSpider(scrapy.Spider):
    name = "gcloud"

    def start_requests(self):
        baseurl = 'https://www.digitalmarketplace.service.gov.uk/g-cloud/services/624695628011497'
        yield scrapy.Request(url=baseurl, callback=self.parse)

    def parse(self, response):
        self.logger.warning(response.url)

        entry = ''
        filename = 'gcloud-services.csv'

        count = 1
        is_div = True
        while is_div:
            count_formatted = str(count).zfill(2)
            try:
                fields = response.xpath(
                    f'//div[contains(@id,"{count_formatted}")]//div[1]//dt//text()')[0].root.strip()
                fields_text = response.xpath(
                    f'//div[contains(@id,"{count_formatted}")]//div[1]//dd//text()')[0].root.strip()

                entry += fields + '\n' + fields_text
                self.logger.warning(entry)

                count += 1
            except:
                is_div = False
                print(f'No div numbered {count_formatted}')

        with open(filename, 'ab') as f:
            f.write(entry.encode('utf-8'))
        self.log('Saved file %s' % filename)
