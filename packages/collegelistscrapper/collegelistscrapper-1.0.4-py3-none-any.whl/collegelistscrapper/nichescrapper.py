import json, re, os, time
from urllib.parse import urlparse, parse_qs
from concurrent import futures
from bs4 import BeautifulSoup
from requests import api

try:
    import pandas as pd
# from bs4 import BeautifulSoup
    import requests
except:
    print("Packages not Found. Please Install Packages: pandas, requests, bs4, html5lib, xlsxwriter")
    print("Run: \npip install pandas\npip install requests\npip install bs4 \npip install html5lib\npip install xlsxwriter ")
    exit()




class NicheScrapper:
    def __init__(self, url=None, filename=None, header=None, printHelful=True):
        self.url = url
        self.filename = filename

        self.api_available = None

        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }
        if header:
            self.header = header

        self.printHelpfulMessage = printHelful

        self.super_list = {
            # To Turn the college object dicts into pandas data frame format
            "Name": [],
            "Location": [],
            "URL": [],
            "Niche Grade": [], #
            "Acceptance Rate": [],
            "SAT Range": [],
            "Net Price": [], #
            "Application Fee": [],
            "SAT/ACT": [],
            "High School GPA": [],
            "ED/EA": [],
            "UnderGrad Students": [],
            "Application Deadline": [],
            "Virtual Tour": [],
            "Majors": [],
            
        }

    def messagePrint(self, txt):
        """ Print Message only if printHelpfulMessage is turned on"""
        if self.printHelpfulMessage:
            print(txt)

    def get_url_queries(self, url, page=None, isAPI=True):
        """Gets get queries from given url, removes page query
        and returns queries as a dict"""
        parsed_url = urlparse(url)
        queries = parse_qs(parsed_url.query)

        try:
            queries.pop("page")
        except KeyError:
            pass

        if page:
            queries["page"] = page

        if isAPI:
            queries["listURL"] = parsed_url.path.split("/")[-2]
            return ("https://www.niche.com/api/renaissance/results/", queries)
        else:
            return (f"https://{parsed_url.hostname}{parsed_url.path}", queries)
 
 
    def is_API(self, url):
        """This function  needs to run once only.
        Then stores result in api_available and returns it."""

        if self.api_available != None:
            return self.api_available

        try:
            self.messagePrint("Checking if API is available...")
            site, query = self.get_url_queries(url, isAPI=True)
            res = requests.get(site, params=query, headers=self.header, timeout=10)

            if res.status_code == 200:
                self.api_available = True
                self.messagePrint("Yeppy, API found.")

                return True
            else:

                self.messagePrint("Sorry, API not Found.")
                self.messagePrint(
                    "But Don't worry we will still try, it might be slow. Have patience."
                )

                self.api_available = False
                return False
        except:
            api_available = False
            return False

    def get_college_entities_list(self, url, pg):
        """ Gets colleges entities list only in one given page"""
        if self.is_API(url):  # IF given url is in API
            site, query = self.get_url_queries(url, page=pg, isAPI=True)
            res = requests.get(site, params=query, headers=self.header, timeout=10)

            if res.status_code == 200:
                self.messagePrint(f"Recieved Colleges List in Page {pg} from API.")

            entities = json.loads(res.text)["entities"]
            # only get entities object from response

        else:
            site, query = self.get_url_queries(url, page=pg, isAPI=False)
            res = requests.get(site, params=query, headers=self.header, timeout=10)

            if res.status_code == 200:
                self.messagePrint(f"Recieved Colleges List in Page {pg} by Scrapping.")

            window_preloaded = (  # See Liberal_raw.js as refrence
                re.findall(r"window.App=.*", res.text)[0]
                # get whole line with tags as well
                .split("</script>")[0]
                # Remove all the tags and get the main script
                .split("window.__PRELOADED_STATE__=")[1]
                # Remove 'window.__PRELOADED_STATE__ everything before it'
                .split("window.__ROM_STATE__")[0][:-1]
                # Remove every other variable except the contents of window.PRELODEDSTATE
                # Then remove semicolon with [:-1]
            )

            dict_window_preloaded = json.loads(window_preloaded)
            entities = dict_window_preloaded["entitySearch"]["response"]["entities"]

        if res.status_code != 200:
            self.messagePrint(
                f"""Some Unkown Error Occured.
                Please contact the developer with screenshot.
                    RESPONSE CODE={res.status_code}
                    URL={res.url}"""
            )
            return False

        return entities

    def get_all_college_entities_list(self, url):
        """ Takes a search url from niche 
        and returns entities of all colleges in search result."""
        self.messagePrint("\n\nGetting Colleges List.")
        main_dataset = []  # Accumulates scarped entities data
        
        # Main process
        with futures.ThreadPoolExecutor() as exe:
            for i in range(1, 110):
                entities = exe.submit(self.get_college_entities_list, url, i)

                if len(entities.result()) ==0:
                    break

                main_dataset = main_dataset + entities.result()
        
        print(f"\n\nCollected {len(main_dataset)} colleges.\n")
        
        return main_dataset

    def retrive_data_from_entity(self, entity, index=None):
        """ Turn the jumbled entity item returned by previous methods.
            Into useful information dict.
         """
        content = entity["content"]
        college_entity = entity["content"]["entity"]

        for fact in content["facts"]:  # Get from facts
            if fact["label"] == "Acceptance Rate":
                accept_rate = f"{(fact.get('value',0)*100)}%"
            elif fact["label"] == "Net Price":
                net_price = fact.get("value", "N/A")
            elif fact["label"] == "SAT Range":
                sat_range = fact.get("value", "N/A")
            else:
                continue

        for i in content["grades"]:  # Get from grades
            if i["label"] == "Overall Niche Grade":
                niche_grade = i.get("value", "N/A")

        for i in content["virtualTour"]:
            if i["label"] == "Virtual Tour":
                tour = i.get("value", "N/A")

        info = {
            "Name": college_entity.get("name", "N/A"),
            "Location": college_entity.get("location", "N/A"),
            "URL": f"https://www.niche.com/colleges/{college_entity.get('url', 'N/A')}",
            "Acceptance Rate": accept_rate if accept_rate else "N/A",
            "Net Price": net_price if net_price else "N/A",
            "SAT Range": sat_range if sat_range else "N/A",
            "Niche Grade": niche_grade if niche_grade else "N/A",
            "Tour": tour if tour else "N/A",
        }
        if index or (index==0):
            self.messagePrint(f"{index}. Recieved General Data for {info['Name']}")
        else:
            self.messagePrint(f"Recieved General Data for {info['Name']}")
        
        return info

    def get_block_in_window_app(self, blocks, anchor):
        """ SPECIAL FUNCATION JUST FOR get_college_specific_data.
        IT TAKES BLOCKS LIST AND RETURNS SPECIFIED BLOCK """
        # anchor is equivalent to id in html page
        for block in blocks:  # find the given anchor block among all blocks
            try:
                if anchor in block["config"]["anchor"]:
                    return block
            except KeyError:
                continue
        
        return dict()

    def get_data_from_block_in_window_app(self, block, label):
        """SPECIAL FUNCATION JUST FOR get_college_specific_data.
        To get Label Information from block in Specific college data"""
        if not block:
            return "N/A"
        for bucket in block["buckets"].values():
            for i in bucket["contents"]:
                try:
                    if i["label"] == label:
                        return i.get("value", "N/A")
                except KeyError:
                    continue
        return "N/A"

    def get_college_specific_data(self, url, info=None, index=None):
        """ Takes Specific Niche page url and 
        returns all useful information or updates given info dict
        """
        # info must contain college Name, Location and stuffs


        self.messagePrint(f"Visting {url}")

        res = requests.get(url, headers=self.header, timeout=60)
        window_app = (  # See colombia.js for refrence
            re.findall(r"window.App=.*", res.text)[
                0
            ]  # get whole line with tags as well
            .split("</script>")[0]  # Remove all the tags
            .split("window.App=")[1]  # Remove 'window.App'
            .split("window.__PRELOADED_STATE__")[0][:-1]
            # Remove every other variable except the contents of window.App Thrn remove semicolon
        )
        window_app_dict = json.loads(window_app)
        blocks = window_app_dict["context"]["dispatcher"]["stores"]["ProfileStore"][
            "content"
        ]["blocks"]

        if not info:
            info = dict()
        
        for key in list(info): # remove keys without information
            if info[key] == "N/A":
                del info[key]

        header_block = self.get_block_in_window_app(blocks, 'header')
        
        if "Name" not in info.keys():
            for bucket in header_block['buckets'].values():
                if "contents" in bucket.keys(): 
                    for content in bucket["contents"]:
                        if "type" in content.keys():
                            if content["type"] == "Name":
                                info.update([("Name",content.get('label', "N/A"))])
                                break
        
        if "Location" not in info.keys():
            for bucket in header_block['buckets'].values():
                if "contents" in bucket.keys(): 
                    for content in bucket["contents"]:
                        if "type" in content.keys():
                            if content["type"] == "Location":
                                info.update([("Location",content.get('value', "N/A") )])
                                break
        
        if "URL" not in info.keys():
            info["URL"] = url

        if "Grade" not in info.keys():
            report_card_block = self.get_block_in_window_app(blocks, 'report-card')
            if "buckets" in report_card_block:
                for bucket in report_card_block["buckets"].values():
                    if "contents" in bucket.keys():
                        for content in bucket["contents"]:
                            if "type" in content.keys():
                                if content["type"] == "Grade":
                                    info.update([("Grade",content.get('value', "N/A"))])
                                    break

        if "Net Price" not in info.keys():
            cost_block = self.get_block_in_window_app(blocks, "cost")
            info["Net Price"] = self.get_data_from_block_in_window_app( cost_block, "Net Price")


        admission_block = self.get_block_in_window_app(blocks, "admissions")
        if "Acceptance Rate" not in info.keys():
            info["Acceptance Rate"] = self.get_data_from_block_in_window_app(
                        admission_block, "Acceptance Rate"
                    )

        if "SAT Range" not in info.keys():
            info["SAT Range"] = self.get_data_from_block_in_window_app(
                        admission_block, "SAT Range"
                    )

        if "Tour" not in info.keys():
            for bucket in header_block['buckets'].values():
                if "contents" in bucket.keys(): 
                    for content in bucket["contents"]:
                        if "label" in content.keys():
                            if content["label"] == "Virtual Tour":
                                info.update([("Tour",content.get('value', "N/A"))])
                                break
        
        if "Tour" not in info.keys() or (info.get("Tour") == None):
            info.update([("Tour", self.get_data_from_block_in_window_app(admission_block, "Application Website"))])
        

        info.update(
            [
                (
                    "Application Deadline",
                    self.get_data_from_block_in_window_app(
                        admission_block, "Application Deadline"
                    ),
                )
            ]
        )
        info.update(
            [
                (
                    "Application Fee",
                    self.get_data_from_block_in_window_app(
                        admission_block, "Application Fee"
                    ),
                )
            ]
        )
        info.update(
            [
                (
                    "SAT/ACT",
                    self.get_data_from_block_in_window_app(
                        admission_block, "SAT\u002FACT"
                    ),
                )
            ]
        )
        info.update(
            [
                (
                    "GPA",
                    self.get_data_from_block_in_window_app(
                        admission_block, "High School GPA"
                    ),
                )
            ]
        )
        info.update(
            [
                (
                    "ED/EA",
                    self.get_data_from_block_in_window_app(
                        admission_block, "Early Decision/Early Action"
                    ),
                )
            ]
        )

        students_block = self.get_block_in_window_app(blocks, "students")

        info.update(
            [
                (
                    "Undergrad Students",
                    self.get_data_from_block_in_window_app(
                        students_block, "Full-Time Enrollment"
                    ),
                )
            ]
        )

        majors_block = self.get_block_in_window_app(blocks, "majors")
        majors_list = []
        if "buckets" in majors_block:
            for bucket in majors_block["buckets"].values():
                if "contents" in bucket.keys():
                    for content in bucket["contents"]:
                        if "entities" in content.keys():
                            for entity in content["entities"]:
                                majors_list.append(entity["name"])
        if majors_list:
            info.update([("Majors", ','.join(majors_list))])
        else:
            info.update([("Majors", "N/A")])
    


        return info

    def apppend_in_superlist(self, info):
        self.messagePrint(f"Adding {info['Name']}data  to superlist.")
        self.super_list["Name"].append(info["Name"])
        self.super_list["Location"].append(info.get("Location", "N/A"))
        self.super_list["URL"].append(info.get("URL", "N/A"))
        self.super_list["Acceptance Rate"].append(info.get("Acceptance Rate", "N/A"))
        self.super_list["Net Price"].append(info.get("Net Price", "N/A"))
        self.super_list["SAT Range"].append(info.get("SAT Range", "N/A"))
        self.super_list["Niche Grade"].append(info.get("Grade", "N/A"))
        self.super_list["Virtual Tour"].append(info.get("Tour", "N/A"))
        self.super_list["Application Fee"].append(
            info.get("Application Fee", "N/A in Niche")
        )
        self.super_list["Application Deadline"].append(info["Application Deadline"])
        self.super_list["SAT/ACT"].append(info.get("SAT/ACT", "N/A in Niche"))
        self.super_list["High School GPA"].append(info.get("GPA", "N/A in Niche"))
        self.super_list["ED/EA"].append(info.get("ED/EA", "N/A in Niche"))
        self.super_list["UnderGrad Students"].append(
            info.get("Undergrad Students", "N/A in Niche")
        )
        self.super_list["Majors"].append(info.get("Majors", "N/A in Niche"))

    def export_excel(self, filename=None):
        filename = filename if filename else self.filename
        # Create pandas dataframe
        df = pd.DataFrame(self.super_list)

        # self.messagePrint("Successful..")
        self.messagePrint(f"Writing {filename}.xlsx")

        # # Create a Pandas Excel writer using XlsxWriter as the engine.
        try:
        # # Convert the dataframe to an XlsxWriter Excel object.
            writer = pd.ExcelWriter(f"{filename}.xlsx", engine="xlsxwriter")
            df.to_excel(writer, sheet_name="Sheet1")
        # # Close the Pandas Excel writer and output the Excel file.
            writer.save()
        
        except ModuleNotFoundError:
            print("Please Install xlsxwriter to write into excel")
    
    def export_csv(self, filename=None):
        df = pd.DataFrame(self.super_list)
        filename = filename if filename else self.filename
        self.messagePrint(f"Writing {filename}.csv")
        df.to_csv(f"{filename}.csv")

    def run(self):
        if os.path.exists(f'{self.filename}_entities.json'):
            with open(f"{self.filename}_entities.json", "r") as file:
                entities = json.loads(file.read())
                df = pd.read_csv(f"{self.filename}_temp.csv", index_col=0)

                print("Retrieving data from saved files.")

                for idx, row in df.iterrows():
                    self.apppend_in_superlist(row)
                    
        else:
            entities = self.get_all_college_entities_list(self.url)
        
        with futures.ThreadPoolExecutor() as executor:
            try:
                for i,entity in enumerate(entities):
                    info = self.retrive_data_from_entity(entity, index=i)
                    info = executor.submit(self.get_college_specific_data, info["URL"], info, i)
                    self.apppend_in_superlist(info.result())
                    self.messagePrint("\n\n")

            
            except KeyboardInterrupt or Exception:
                entities = entities[i:]
                with open(f"{self.filename}_entities.json", "w") as file:
                    file.write(json.dumps(entities))
            
                self.export_csv(filename=f"{self.filename}_temp")
                exit()

        self.export_excel()
        if os.path.exists(f"{self.filename}_entities.json"):
            os.remove(f"{self.filename}_entities.json")
        if os.path.exists(f"{self.filename}_temp.csv"):
            os.remove(f"{self.filename}_temp.csv")
        
        print("\n\n\nAll Done :).\n Even if N\A written, data may be available in Niche. Be optimist and Check in Niche First.")
        


if __name__ == "__main__":
    # Take Input from User
    url = input("Enter the url :")
    filename = input("Enter filename to save :")
    obj = NicheScrapper(url=url, filename=filename)
    obj.run()