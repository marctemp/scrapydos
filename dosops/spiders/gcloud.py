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
        countstr = str(count)
        countfill = countstr.zfill(2)
        while countfill < str(22):
            field = response.xpath('//div[contains(@id,"'+ countfill + '")]//div[1]//text()')
            field_text = response.xpath('//div[contains(@id,"01")]//div[1]//dd//text()')
            count += 1
            entry += field + '\n' + field_text
            self.logger.warning(entry)
            with open(filename, 'ab') as f:
                f.write(entry.encode('utf-8'))
            self.log('Saved file %s' % filename)
