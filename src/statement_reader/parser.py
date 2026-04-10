from PyPDF2 import PdfReader
from .models import Transaction

#Used to find the beginning of the "Standard Purchases" list in Citi PDF. Date is in format MM/DD
def is_date(string):
    if len(string) != 5:
        return False
    if string[2] != '/':
        return False
    return True

#Used to find the end of the "Standard Purchases" list in Citi PDF. Price is in format $XX.XX
def is_price(string):
    if string == "":
        return False
    if string[0] != '$':
        return False
    if string.find('.') == -1:
        return False
    return True
    
    
def clean_transaction(item, year):
    #removes $ from front of price
    item["Price"] = item["Price"][1:]
    #puts date into format of YYYY-MM-DD
    item["Date"] = year + "-" + item["Date"][:2] + "-" + item["Date"][3:]
    

#looks for date in format MM/DD/YY
def found_year(string):
    print(string)
    if string == "":
        return False
    if len(string) != 8:
        return False
    if string[2] != '/':
        return False
    return True
 
 #Sorry to any statements before the turn of the century /:
def create_year(string):
    year = "20" + string[6:]
    return year
    
    #removes everything after the substring
def slicer(my_str,sub):
    index = my_str.lower().find(sub)
    if index != -1:
        return my_str[:index]
    else:
        raise Exception("Sub string not found!")    

def parse(file):
    reader = PdfReader(file.file)

    transaction_page = reader.pages[2]
    year_page = reader.pages[0]

    year_page = year_page.extract_text().split("Payment due date", 1)[1]
    year_page = year_page.split("\n")
   
    text = transaction_page.extract_text().split("Standard P", 1)[1]
    text = slicer(text, "fees charged")

    res = text.split('\n')

    while is_date(res[0]) == False:
       res.pop(0)

    while is_price(res[len(res)-1]) == False:
       res.pop(len(res) - 1)
    
    while found_year(year_page[0]) == False:
        year_page.pop(0)

    year = create_year(year_page[0])

    list_of_transactions = []
    
    #reads through Standard Purchases table
    while res:
       date = res.pop(0)
       temp = res.pop(0)
       name = res.pop(0)
       price = res.pop(0)
       list_of_transactions.append({"Name": name, "Price": price, "Date": date})

    for transaction in list_of_transactions:
        clean_transaction(transaction, year)
        
        trans = Transaction()
        trans.vendor_name = transaction["Name"]
        trans.amount = transaction["Price"]
        trans.date = transaction["Date"]
        trans.save()
        