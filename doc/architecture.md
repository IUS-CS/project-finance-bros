# Statement Reader Architecture

Statement Reader is a a Django web application. 

## Systems Overview

Everything is handled within Django. The application, Statement_Reader, holds the functionality and visuals of the website. The Views render the HTML Templates. Additionally, the Views, through the Transaction Model that is connected to the Transaction Schema, is able to output from the SQLite Database. Furthermore, the Forms get the fields from the Transaction Model and is also connected to the Views. When a Form is saved in a View, it gets inserted into the database. The URLs are created from the Views. Finally, the "manage.py" file is used for deployment and admin purposes.

![Thing](/doc/images/architecture/SystemsArchitecture.png?raw=true)

## Database Schema

The Transaction Schema contains the fields "id," "vendor_name," "date," and "amount." The "id" field is automatically created and assigned to each transaction for a unique identification. The "vendor_name" is a string. The "date" is a date value. Lastly, "amount" is a decimal.

![Thing](/doc/images/architecture/DatabaseModel.png?raw=true)

## User Flow
When accessing the website, the user is, first, at the home page. From there, they can either go to the statement reader, enter a new transaction, or see a list of all of their transactions. If they go to the statement reader, they will be able to upload their credit card statement as a PDF. On the other hand, if they choose to enter a transaction, they will enter the information and submit. This takes them to the page where they can see their new transaction, along with their previous ones. Now, the user can go back to edit a transaction's information or delete one from the list. At each of the three pages, they can go back to the home page.

![Thing](/doc/images/architecture/UserFlow.png?raw=true)

## Database Interaction
When submitting a transaction's information, this gets inserted into the database. When the list of transactions loads, including the recently submitted one, the page is outputting from the "TransactionSchema." If a user decides to delete one of their transactions, the record within the schema is deleted. Then, the page reloads with the new list after the removal. If a user decides to edit the information on one of their transactions, the input page retreives the data from the schema. When submitting with the new information, the record is updated in the schema. Then, the list page loads, outputting the new transaction records.

![Thing](/doc/images/architecture/DatabaseInteraction.png?raw=true)

## Deployment
When deploying the application, a virtual environment is created so that the "manage.py" file is able to execute the "runserver" command. This creates a local server on the user's device. From here, they can open up a web browser and enter the "localhost" URL. Now, they can access the web application.

![Thing](/doc/images/architecture/Deployment.png?raw=true)