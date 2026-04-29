# Testing

For unit tests, we utilized Django's test.py file. This can be run with the "python manage.py test" command. We included tests for entering, editing, and deleting transactions. Additionally, we included tests for uploading PDF statements. There are also edge case tests for checking that the action will fail if the user inputs incorrectly.

For the system test, we used PlayWright This can be run with the "pytest" command, while the server is running. We included tests for entering, editing, and deleting transactions by verifing that the elements are rendered on the browser's page. 
