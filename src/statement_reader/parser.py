from PyPDF2 import PdfReader
from .models import Transaction

def is_date(string):
    if len(string) != 5:
        return False
    if string[2] != '/':
        return False
    return True

def is_price(string):
    if string == "":
        return False
    if string[0] != '$':
        return False
    if string.find('.') == -1:
        return False
    return True
    
    
def clean_item(item, year):
    #removes $ from front of price
    item["Price"] = item["Price"][1:]
    #puts date into format of YYYY-MM-DD
    item["Date"] = year + "-" + item["Date"][:2] + "-" + item["Date"][3:]
    

def found_year(string):
    print(string)
    if string == "":
        return False
    if len(string) != 8:
        return False
    if string[2] != '/':
        return False
    return True
 
def create_year(string):
    year = "20" + string[6:]
    return year
    

def parse(file):
    reader = PdfReader(file.file)

    tet = reader.pages[2]
    tet2 = reader.pages[0]

    year = tet2.extract_text().split("Payment due date", 1)[1]
    year = year.split("\n")
    

    text = tet.extract_text().split("Standard P", 1)[1]

    #removes everything after the substring
    def slicer(my_str,sub):
       index = my_str.lower().find(sub)
       if index != -1:
          return my_str[:index]
       else:
          raise Exception("Sub string not found!")


    text = slicer(text, "fees charged")

    res = text.split('\n')

    while is_date(res[0]) == False:
       res.pop(0)

    while is_price(res[len(res)-1]) == False:
       res.pop(len(res) - 1)
    
    while found_year(year[0]) == False:
        year.pop(0)

    year = create_year(year[0])

    print(year)
    

    list = []

    while res:
       date = res.pop(0)
       temp = res.pop(0)
       name = res.pop(0)
       price = res.pop(0)
       list.append({"Name": name, "Price": price, "Date": date})

    for item in list:
        
        clean_item(item, year)
        
        trans = Transaction()
        trans.vendor_name = item["Name"]
        trans.amount = item["Price"]
        trans.date = item["Date"]
        trans.save()
        
  