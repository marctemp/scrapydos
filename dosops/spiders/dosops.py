from datetime import datetime as dt
from pandas import read_csv
from tqdm import tqdm
import scrapy


class DosOpsSpider(scrapy.Spider):

    timestamp = dt.now().strftime('%Y-%m-%dT%H-%M-%S')
    name = 'dosops'
    base_url = 'https://www.digitalmarketplace.service.gov.uk/digital-outcomes-and-specialists/opportunities/'

    digOut_fields = ['Published', 'Deadline for asking questions', 'Closing date for applications', 'Summary of the work',
                     'Latest start date', 'Expected contract length', 'Location', 'Organisation the work is for',
                     'Budget range', 'Why the work is being done', 'Problem to be solved', 'Who the users are and what they need to do',
                     'Early market engagement', 'Any work that\'s already been done', 'Existing team', 'Current phase',
                     'Address where the work will take place', 'Working arrangements', 'Security clearance', 'Additional terms and conditions',
                     'Essential skills and experience', 'Nice-to-have skills and experience', 'How many suppliers to evaluate', 'Proposal criteria',
                     'Cultural fit criteria', 'Payment approach', 'Assessment methods', 'Evaluation weighting']

    digSpe_fields = ['Published', 'Deadline for asking questions', 'Closing date for applications', 'Specialist role',
                     'Summary of the work', 'Latest start date', 'Expected contract length', 'Location',
                     'Organisation the work is for', 'Maximum day rate', 'Early market engagement', 'Who the specialist will work with',
                     'What the specialist will work on', 'Address where the work will take place', 'Working arrangements', 'Security clearance',
                     'Additional terms and conditions', 'Essential skills and experience', 'Nice-to-have skills and experience', 'How many specialists to evaluate',
                     'Cultural fit criteria', 'Assessment methods', 'Evaluation weighting']

    research_fields = ['Published', 'Deadline for asking questions', 'Closing date for applications', 'Summary of the work',
                       'Location', 'Research dates', 'Organisation the work is for', 'Budget range',
                       'Early market engagement', 'Description of your participants', 'Assisted digital and accessibility requirements', 'Research plan',
                       'Research location', 'Access restrictions at location', 'Number of research rounds', 'Number of participants per round',
                       'How often research will happen', 'Evening or weekend research', 'Additional terms and conditions', 'Essential skills and experience',
                       'Nice-to-have skills and experience', 'How many suppliers to evaluate', 'Proposal criteria', 'Assessment methods',
                       'Evaluation weighting']

    path = '/Users/marcte/Documents/_Development/Procurement/data/DOS.csv'

    def start_requests(self, ids=None):
        if not ids:
            ids = load_ids()
        for id in tqdm(ids):
            yield scrapy.Request(url=self.base_url + str(id), callback=self.parse)

    def check_page(self, response, xpath):
        if self.extract_website(response, xpath).extract_first() != None:
            return True
        else:
            return False

    def check_xpath(self, extract_website):
        if extract_website.extract_first() != '\n        ':
            return True
        else:
            return False

    def extract_website(self, response, xpath):
        return response.selector.xpath(xpath)

    def extract_web_elements(self, extract_website, delim='}}'):
        extract = [extract_website[i].get().strip()
                   for i in range(len(extract_website))]
        extract = '}}'.join(extract)
        return extract.strip()

    def extract_xpath(self, response, entry, xpath_base, xpath_ext='"]/../dd/text()'):
        xpath = xpath_base + xpath_ext
        extract_website = self.extract_website(response, xpath)

        if self.check_xpath(extract_website):
            entry += '\t' + self.extract_web_elements(extract_website)
            return entry

        xpath = xpath_base + '"]/../dd/*/*/text()'
        extract_website = self.extract_website(response, xpath)
        if self.check_xpath(extract_website):
            entry += '\t' + self.extract_web_elements(extract_website)
            return entry

        entry += '\t' + 'UNDEFINED'
        return entry

    def parse(self, response):
        title = response.css('h1::text').extract_first()
        entry = title

        entry = self.extract_xpath(response, entry,
                                   '//section[@class="dm-banner"]', '/*/text()')

        digSpe_xpath = self.xpath_stylisation('Specialist role')
        research_xpath = self.xpath_stylisation('Research plan')

        if self.check_page(response,
                           '//dt[text()="' + digSpe_xpath + '"]/../dd/text()'):
            datapoints = list(map(self.xpath_stylisation, self.digSpe_fields))
            filename = self.timestamp + 'digspe.tsv'
        elif self.check_page(response,
                             '//dt[text()="' + research_xpath + '"]/../dd/text()'):
            datapoints = list(
                map(self.xpath_stylisation, self.research_fields))
            filename = self.timestamp + 'res.tsv'
        else:
            datapoints = list(map(self.xpath_stylisation, self.digOut_fields))
            filename = self.timestamp + 'dosops.tsv'

        for datapoint in tqdm(datapoints):
            if self.xpath_stylisation('Evaluation weighting') == datapoint:
                entry = self.extract_xpath(response,
                                           entry,
                                           '//dt[text()="' + datapoint, '"]/../dd/*/text()')
            entry = self.extract_xpath(response,
                                       entry,
                                       '//dt[text()="' + datapoint)

        entry += '\t' + response.url.split('/')[-1] + '\n'
        self.logger.warning(entry)

        with open(filename, 'ab') as f:
            f.write(entry.encode('utf-8'))
        self.log('Saved file %s' % filename)
