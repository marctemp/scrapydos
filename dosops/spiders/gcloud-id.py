import scrapy

class GCloudIDSpider(scrapy.Spider):
    name = 'gcloud-ids'

    def start_requests(self):
        baseurl = 'https://www.digitalmarketplace.service.gov.uk/g-cloud/search?page='
        for x in range(1,1279):
            yield scrapy.Request(url=baseurl + str(x), callback=self.parse)

    def parse(self, response):
        self.logger.warning(response.url)
        entry = ''
        filename = 'gcloud-ids.csv'
        for section in response.selector.xpath('//div[@id="js-dm-live-search-results"]'):
            service_id = section.xpath('//a[@class="govuk-link"]/@href')[5:]
            for select in service_id:
                entry += select.root
                entry += '\n'
            with open(filename, 'ab') as f:
                f.write(entry.encode('utf-8'))
        self.log('Saved file %s' % filename)
 