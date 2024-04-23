from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

from oauth2client.service_account import ServiceAccountCredentials

from datetime import datetime

import csv, gspread, os, re, time, traceback

class FillOutForm:
    
    def __init__(self):
        
        service = Service(executable_path=r"D:\\selenium\\chromedriver.exe")
        self.driver = webdriver.Chrome(service=service)
        
        self.file_settings = "settings.cfg"
        
        self.settings = None
        
        self.success = 0 #Stores progress
        self.site = None #Stores website URL
        self.elements = None #Stores form IDs
        self.biggest = 0 #Stores biggest ID number
        self.data = None #Stores CSV data
        self.fsubs = 0 #Counts amount of times form submitted
        self.current_row = None #Stores current row from CSV
        

        
        self.categories = [  {"type":"Analytics","value":"8"},
        					 {"type":"Communication","value":"9"},
        					 {"type":"Company","value":"7"},
        					 {"type":"Language","value":"6"},
        					 {"type":"Management","value":"5"},
        					 {"type":"Programmers","value":"4"},
        					 {"type":"Programs","value":"3"},
        					 {"type":"University","value":"2"} ] #Stores categories and their values 

        self.cfg_driver = None
        self.cfg_csvfile = None
        self.cfg_site = None
        self.cfg_user = None
        self.cfg_pass = None
        self.cfg_header = None
        self.cfg_showsettings = None  
        self.cfg_google = None
        self.client = None
        
    def connectGoogle(self):
        
        try:
        
            scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
            
            creds = ServiceAccountCredentials.from_json_keyfile_name(self.cfg_google, scope)
            
            self.client = gspread.authorize(creds)
            
        except Exception as e:
            error_message = traceback.format_exc()
            self.logit((e,":",error_message))
            
 
    #adding timestamp console output
    def logit(self,data):

        current_datetime = datetime.now()

        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        with open("formsubmit.log", "a") as myfile:
            print(formatted_datetime,data)
            myfile.write(formatted_datetime+" : "+str(data)+"\n")           
        
    def load_settings(self):
        
        try:
            with open(self.file_settings) as j:
                content = j.readlines()
                self.settings_found = 1
                
            self.settings = [x.strip() for x in content];
            
        except:
            self.logit(("ERROR: getting settings failed or not found"))
            self.settings_found = 0
            
            self.settings = []
            self.settings.append("driver=C:\pathto\chromedriver.exe")
            self.settings.append("csvfile=C:\pathto\mycsvfile.csv")
            self.settings.append("site=https://yoursite.url")
            self.settings.append("user=username")
            self.settings.append("pass=password")
            self.settings.append("google=C:\pathto\google.json")
            self.settings.append("showsettings=1")
            self.settings.append("header=1")

            if not os.path.exists(self.file_settings):
                
                self.logit(("creating default settings file..."))
                
                with open(self.file_settings, "w") as myfile:
                    myfile.write("")    
                
                for setting in self.settings:
        
                    with open(self.file_settings, "a") as myfile:
                        myfile.write(setting+"\n")     
                        
        try:
            
            #extracting settings
            for line in self.settings:
                
                if not line.startswith("#"):
                
                    line_split = line.split("=")
                    
                    if line_split[0] == "driver" : 
                        self.cfg_driver = line_split[1].strip() 
                        
                    if line_split[0] == "csvfile" : 
                        self.cfg_csvfile = line_split[1].strip()

                    if line_split[0] == "site" : 
                        self.cfg_site = line_split[1].strip()   
                        
                    if line_split[0] == "user" : 
                        self.cfg_user = line_split[1].strip() 

                    if line_split[0] == "pass" : 
                        self.cfg_pass = line_split[1].strip()  
                        
                    if line_split[0] == "google" : 
                        self.cfg_google = line_split[1].strip()                          

                    if line_split[0] == "header" : 
                        self.cfg_header = line_split[1].strip()                         

                    if line_split[0] == "showsettings" : 
                        self.cfg_showsettings = line_split[1].strip()                    
 
        except Exception as e:
            error_message = traceback.format_exc()
            self.logit((e,":",error_message))

        self.logit(("Settings:"))
        self.logit(("--------"))
        self.logit(("cfg_driver:",self.cfg_driver))
        self.logit(("cfg_site:",self.cfg_site))
        self.logit(("cfg_user:",self.cfg_user))
        self.logit(("cfg_pass:",self.cfg_pass))
        self.logit(("cfg_google:",self.cfg_google))
        self.logit(("cfg_csvfile:",self.cfg_csvfile))
        self.logit(("cfg_header:",self.cfg_header))
        self.logit(("cfg_showsettings:",self.cfg_showsettings))
        self.logit(("--------"))

    #Match category
    def find_category_value(self, input_cat):
        for category in self.categories:
            if category['type'] == input_cat:
                return category['value']
        return None

    #Used for page load waitining instead of WebDriverWait
    def wait(self,a=10):
        time.sleep(a)
        
    #Opens the website with WebDriver
    def navigate(self):
        
        if self.cfg_site:

            self.driver.get(self.cfg_site)
            self.logit(("Navigated to:", self.driver.current_url))
            
        else:
            self.logit(("Error: URL not provided"))
    
    #This method will search of certain elements and store them, since the page always adds dynamic element ID names.          
    def find_elements(self):

        self.logit(("Finding Elements for Login..."))

        xpath_expression = "//form[contains(@class,'wpqa_form') and contains(@class,'login-form') and contains(@class,'wpqa_login')]//input[@name='log' and contains(@id, 'username_')]"

        elements = self.driver.find_elements(By.XPATH, xpath_expression)
        
        the_ids = []

        for element in elements:
            the_id = element.get_attribute('id')
            the_ids.append(the_id)

        for element in the_ids:
            
            biggest = 0

            the_num = int(element.split("_")[1])
            
            if the_num > biggest : 
                
                biggest = the_num
                
        self.biggest = biggest

        ifield_usr = "username_"+str(self.biggest)
        ifield_pwd = "password_"+str(self.biggest)
        
        self.elements = {"user": ifield_usr, "pass": ifield_pwd}
            
        self.logit(("Elements: ",self.elements))
   
    #This method will search of certain elements and store them, since the page always adds dynamic element ID names. 
    def find_elements2(self):
        
        self.logit(("Finding Elements for Form Fill..."))
          
        self.elements = {}
        
        xpath_expression = "//form[contains(@class,'wpqa_form') and contains(@class,'form-post')]//input[contains(@id, 'question')]"

        elements = self.driver.find_elements(By.XPATH, xpath_expression)
        
        the_ids = []

        for element in elements:
            the_id = element.get_attribute('id')
            
            if "question-title-" in the_id or "question-category--" in the_id or "question_tags-" in the_id or "question-details-add-" in the_id: 
                
                if not the_id.startswith("qt"):
                
                    the_ids.append(the_id)
            
        for element in the_ids:
            
            biggest = 0
            
            the_string = re.findall(r'\d+', element)

            the_num = int(the_string[0])
            
            if the_num > biggest : 
                
                biggest = the_num
                
        self.logit(("biggest:",biggest))
        
        #We take the biggest number value used in ID creation
        self.biggest = biggest
        
        ifieldt_title = "question-title-"+str(self.biggest)
        ifieldt_category = "question-category-"+str(self.biggest)
        ifieldt_question_tags = "question_tags-"+str(self.biggest)
        ifieldt_comment = "question-details-add-"+str(self.biggest)
        
        self.elements = {"title": ifieldt_title, "cat": ifieldt_category, "tags" : ifieldt_question_tags, "comment" : ifieldt_comment}
            
        self.logit(("Elements: ",self.elements))       

    #Method to log in
    def log_in(self):
        
        
        
        self.navigate() #load site
        self.find_elements() #find form elements
        
        if len(self.elements) == 2:

            self.logit(("Checking log in...",self.elements))
            
            self.driver.execute_script("document.getElementById('" + self.elements["user"] + "').value = '';")
            self.success = 1
 
        if self.success == 1:

            try:
                
                self.logit(("Trying to log in...",self.elements))

                input_user = self.driver.find_element(By.ID, self.elements["user"])
                input_pass = self.driver.find_element(By.ID, self.elements["pass"])

                input_user.send_keys(self.cfg_user)
                input_pass.send_keys(self.cfg_pass)
                
                self.driver.save_screenshot('login.png')
                
                input_pass.send_keys(Keys.ENTER)
                
                self.wait()
                self.logit(("Successfully logged in!"))
                self.driver.save_screenshot('login_submitted.png')
                self.success = 2

            except Exception as e:
                error_message = traceback.format_exc()
                self.logit((e,":",error_message))
                
    #Getting CSV data         
    def getdata(self):
        
        
        if self.cfg_csvfile.lower().endswith(".csv"):

            data = []
            with open(self.cfg_csvfile, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
    
                first_row = next(reader)
                has_header = first_row[0].startswith("Title")
        
                if not has_header:
                    data.append({"Title": first_row[0], "Category": first_row[1], "Tags": first_row[2], "Comment": first_row[3]})
                
                for row in reader:
                    data.append({"Title": row[0], "Category": row[1], "Tags": row[2], "Comment": row[3]})
        
            self.data = data
            
        else:
            data = []

            sheet = self.client.open_by_key(self.cfg_csvfile).sheet1   
            
            all_values = sheet.get_all_values()

            for line in all_values:
                
                if line[0] != "Title":
                    
                    data.append({"Title": line[0], "Category": line[1], "Tags": line[2], "Comment": line[3]})
            
            
            self.data = data
            
            print("Data Available:\n",self.data)
            

    #Loop to run CSV data
    def run_data(self):
        
        self.getdata()
        
        for line in self.data:
            
            self.current_row = line
            
            self.logit(("Adding:",self.current_row," ..."))
    
            self.find_elements2()
            
            self.fill_out_form()
            
            self.navigate()        

    def fill_out_form(self):        
        
        if len(self.elements) == 4 and self.success == 2:
            
            self.logit(("Checking form..."))

            self.driver.execute_script("document.getElementById('" + self.elements["title"] + "').value = '';")
            self.success = 3 
            
            self.logit(("Form found!"))
            
        if self.success == 3:            
        
            try:
                
                self.logit(("Filling out Form..."))
                
                id_title = self.elements["title"]
                id_cat = self.elements["cat"]
                id_tags = self.elements["tags"]
                id_comment = self.elements["comment"]
                
                data_cat = self.find_category_value(self.current_row["Category"])
                data_title = self.current_row["Title"]
                data_tags = self.current_row["Tags"]
                data_comment = self.current_row["Comment"]                
                
                self.driver.execute_script("document.getElementById('"+id_cat+"').value = '"+str(data_cat)+"';")
                self.logit(("cat sent..."))
                self.driver.execute_script("document.getElementById('"+id_tags+"').value = '"+data_tags+"';")
                self.logit(("tags sent..."))
                self.driver.execute_script("document.getElementById('"+id_comment+"').value = '"+data_comment+"';")
                self.logit(("comment sent..."))
                
                for_button = self.driver.find_element(By.ID, id_title)
                
                self.logit(("-------------"))
                self.logit(("title:",id_title,data_title,self.driver.execute_script("document.getElementById('"+id_title+"').value")))
                self.logit(("cat:",id_cat,data_cat,self.driver.execute_script("document.getElementById('"+id_cat+"').value")))
                self.logit(("tags:",id_tags,data_tags,self.driver.execute_script("document.getElementById('"+id_tags+"').value")))
                self.logit(("comment:",id_comment,data_comment,self.driver.execute_script("document.getElementById('"+id_comment+"').value")))
                self.logit(("-------------"))
                
                self.logit(("Form filled!"))
                self.logit((""))
                
                self.driver.save_screenshot('form_filled.png')
                
                for_button.send_keys(Keys.ENTER) 
                
                self.wait(5)
                
                self.fsubs+=1

                self.driver.save_screenshot('form_submitted_'+str(self.fsubs)+'.png')
                self.logit(("Form submitted!"))

            except Exception as e:
                error_message = traceback.format_exc()
                self.logit((e,":",error_message))
                            
    def web_quit(self):
        self.driver.quit()                

def main():
    f = FillOutForm()
    f.load_settings()
    f.connectGoogle()
    f.getdata()
    f.log_in(f.cfg_user, f.cfg_pass)
    f.run_data()
    f.web_quit()

if __name__ == "__main__":
    main()