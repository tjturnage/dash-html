import re
from datetime import datetime
import requests
import os

try:
    from bs4 import BeautifulSoup
except:
    print("can't import bs4!")

try:
    os.listdir('/usr')
    output_path = '/home/tjt/public_html/public/afd/afds.txt'
except:
    output_path = 'C:/data/scripts/AFDS/afds.txt'
    
class AFD:
    def __init__(self,versions=50):
        self.versions = int(versions)
        if self.versions > 50:
            self.versions = 50
        self.master = []
        self.all_text = []
        self.final = []
        self.update = False    
        self.discussion = False
        self.discussion_done = False
        self.grab_bulletins()
        self.parse_data()
        self.create_text()
        #url = "https://forecast.weather.gov/product.php?site=GRR&issuedby=GRR&product=AFD&format=ci&version=4&glossary=0"

    def grab_bulletins(self):
        for version in range(1,self.versions):
            url = 'https://forecast.weather.gov/product.php?site=GRR&issuedby=GRR&product=AFD&format=ci&version={}&glossary=0'.format(str(version))
            try:
                page = requests.get(url, timeout=5)
                soup = BeautifulSoup(page.content, 'html.parser')
                dat = str(soup.pre)
                self.all_text.append(dat)
            except:
                pass
        return

    def get_time2(self,line):
        """
        input:
            String: "Issued at" line (Ex: 'Issued at 307 AM EST Sat Dec 18 2021')
            return: datestring
            %I      7   Hour (12-hour clock) as a decimal number. (Platform specific)
            %M     06   Minute as a zero-padded decimal number.
            %p     AM   Locale’s equivalent of either AM or PM.
            %a    Sun   Weekday as locale’s abbreviated name.
            %b    Sep   Month as locale’s abbreviated name.
            %-d     8   Day of the month as a decimal number. (Platform specific)
            %Y   2013   Year with century as a decimal number.

        """
        #test = 'Issued at 1207 PM EST Sat Dec 8 2021'
        elements = line.split(" ")
        # remove the time zone and day of week because they don't matter
        extracted_elements = elements[2:4] + elements[6:]
        test2 = " ".join(extracted_elements)
        dt = datetime.strptime(test2, '%I%M %p %b %d %Y')
        dt_str = datetime.strftime(dt, '%Y%m%d%H%M')
        return dt_str
    
    def prettify_name(self,line):
        """
        extracts forecaster id and add dashes and line feeds around it to make it stand out
        """
        buffer = '  --------------------------  '
        fcstr = str(line.split("...")[-1])
        final = f'\n\n{buffer}{fcstr}{buffer}\n\n'
        return final
        
    def parse_data(self):
        for t in range(0,len(self.all_text)):
            get_initials = False
            update_text = []
            discussion_text = []
            text = self.all_text[t]
            lines = text.splitlines()
            discussion_forecaster = ''
            update_forecaster = ''
            update_time = ''
            discussion_time = ''
            for line in lines:
                if ".UPDATE" in line:            
                    self.update = True
                    update_text.append(line)
                    continue
                    
                if ".DISCUSSION" in line:            
                    self.discussion = True
                    discussion_text.append(line)
                    continue
                    
                if "&amp;&amp;" in line:
                    if self.update:
                        self.update = False
                    elif self.discussion:
                        self.discussion = False
                        get_initials = True
                    continue
                    
                if "&amp;&amp;" not in line:
                    if self.update:
                        update_text.append(line)
                        if 'Issued at' in line:
                            update_time = self.get_time2(line)
                            #update_time = self.get_time(line)
                    elif self.discussion:
                        discussion_text.append(line)
                        if 'Issued at' in line:
                            discussion_time = self.get_time2(line)
                            #discussion_time = self.get_time2(line)
                    elif get_initials:
                        if "DISCUSSION..." in line:
                            discussion_forecaster = self.prettify_name(line)
                        if "UPDATE..." in line:
                            update_forecaster = self.prettify_name(line)

            try:
                self.master.append([str(update_time),str(update_forecaster),update_text])
            except:
                pass
            try:
                self.master.append([str(discussion_time),str(discussion_forecaster),discussion_text])
            except:
                pass            

        return


    def create_text(self):
        time_check = []
        for m in range(0,len(self.master)):
            this_one = self.master[m]
            if this_one[0] not in time_check:
                time_check.append(this_one[0])
                self.final.append(self.master[m])
            else:
                pass

        final_sorted = sorted(self.final,reverse=True)
        with open(output_path,'w') as fout:
            for s in range(0,len(final_sorted)):
                this_line = final_sorted[s]
                text = [this_line[1]] + this_line[2]
                output = "\n".join(text)
                print(output)
                fout.write(output)
        return
        
if __name__ == '__main__':
    test = AFD(40)
