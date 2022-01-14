import os
import glob
from collections import Counter
from datetime import date

import requests
import spacy
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

from .pdf import PDF


class PullJob:
    def __init__(self, url, file, noun_num, verb_num):
        self.url = url
        self.file = file
        self.noun_num = noun_num
        self.verb_num = verb_num
        self.body = []
        self.body_string = ''
        self.title = ''
        self.company = ''
        self.city = ''
        self.common_nouns = []
        self.common_verbs = []
        self.common_list = []
        self.cwd = os.getcwd() + '/docs/*'
        self.html = ''

    def scrape(self):
        page = requests.get(self.url)
        if page.status_code == 200:
            self.html = page.text
            print('requested')
        else:
            print('error loading page')

    def get_file(self):
        print('parsing file...')
        soup = BeautifulSoup(self.html, 'html.parser')
        self.title = soup.find('h1').string.replace("\n", "").strip()
        self.company = soup.find('a', class_='topcard__org-name-link '
                                             'topcard__flavor--black-link'
                                 ).text.replace("\n", "").strip()
        self.city = soup.find('span', class_='topcard__flavor '
                                             'topcard__flavor--bullet'
                              ).string.replace("\n", "").strip()
        content = soup.find(
            'div', class_='show-more-less-html__markup '
                          'show-more-less-html__markup--clamp-after-5')
        strong_soup = content.find_all('strong')
        li_soup = content.find_all('li')
        strong_list = [x.text for x in strong_soup]
        li_list = [x.text for x in li_soup]

        for x in iter(content.stripped_strings):
            if x in strong_list:
                self.body.append(' ')
                self.body.append(x)
            elif x in li_list:
                self.body.append(' - ' + x)
            else:
                self.body.append(' ')
                self.body.append(x)

    def write_text(self):
        with open(f"docs/{self.file}.txt", 'w') as fp:
            for x in iter(self.body):
                self.body_string = self.body_string + x
                fp.write(x + '\n')
            fp.close()

    def frequency(self):
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(self.body_string)

        nouns = [token.text
                 for token in doc
                 if (not token.is_stop and
                     not token.is_punct and
                     token.pos_ == "NOUN")]

        verbs = [token.text
                 for token in doc
                 if (not token.is_stop and
                     not token.is_punct and
                     token.pos_ == "VERB")]

        noun_freq = Counter(nouns)
        verb_freq = Counter(verbs)

        self.common_nouns = noun_freq.most_common(self.noun_num)
        self.common_verbs = verb_freq.most_common(self.verb_num)
        self.common_list = self.common_nouns + self.common_verbs

        self.horizontal_chart()

    def horizontal_chart(self):
        word_list, word_occurance = zip(*self.common_list)
        plt.figure(0)  # Specify differnt figures
        plt.rcdefaults()
        plt.barh(word_list, word_occurance)
        plt.title('Most common words')
        plt.ylabel('Word')
        plt.xlabel('Occurance')
        plt.tight_layout()  # add padding
        plt.savefig(f'docs/{self.file}.png')

    def verb_pie_chart(self):
        verb_list, verb_occurance = zip(*self.common_verbs)
        plt.figure()  # Specify differnt figures
        plt.title('Most common Verbs')
        plt.pie(
            verb_occurance, labels=verb_list, autopct='%1.1f%%', shadow=True,
            startangle=90)
        plt.savefig(f'docs/verb_{self.file}.png')

    def noun_pie_chart(self):
        noun_list, noun_occurance = zip(*self.common_nouns)
        plt.figure()  # Specify differnt figures
        plt.title('Most common Nouns')
        plt.pie(
            noun_occurance, labels=noun_list, autopct='%1.1f%%', shadow=True,
            startangle=90)
        plt.savefig(f'docs/noun_{self.file}.png')

    def create_PDF(self):
        print('creating report...')
        today = date.today().strftime('%m/%d/%y')
        # Importing PDF class made in report.py
        pdf = PDF()
        pdf.set_title(f'{self.title} Job Report')
        pdf.set_author('David Hay')
        pdf.print_job(
            today, self.title, self.company, self.city,
            f'docs/{self.file}.txt', self.file)
        pdf.output(f'report/{self.file}.pdf')

    def delete_files(self):
        all_docs = glob.glob(self.cwd)
        for f in all_docs:
            os.remove(f)

    def run_all(self):
        self.scrape()
        self.get_file()
        self.write_text()
        self.frequency()
        self.horizontal_chart()
        self.verb_pie_chart()
        self.noun_pie_chart()
        self.create_PDF()
        self.delete_files()  # If you want to keep other files take out line
        print('Done!')
