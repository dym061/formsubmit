# Form Submit

The Python Form Submit script automates the process of logging into a website, extracting form element IDs dynamically, and filling out and submitting forms based on data from a CSV file or Google Sheets. It uses the Selenium WebDriver for browser interactions, OAuth2 for Google API authentication, and handles errors and logs actions with detailed timestamps. The script is capable of handling dynamic element IDs on the webpage and includes error handling and logging to ensure smooth automation of the form submission process.

## Features

- **Browser Automation**: Utilizes Selenium WebDriver for automating browser interactions, specifically for navigating web pages and manipulating form elements.
- **Dynamic Element Identification**: Dynamically finds and stores web element IDs required for login and form submission processes, accommodating changes in element IDs on the web page.
- **Data Handling**: Supports importing data from both CSV files and Google Sheets to use in form submissions, adapting to different data storage methods.
- **Google API Integration**: Uses OAuth2 authentication with the Google API to access and manipulate Google Sheets, expanding its data handling capabilities.
- **Form Submission**: Automatically fills out and submits web forms using the imported data, streamlining repetitive tasks and improving efficiency.
- **Error Handling and Logging**: Implements robust error handling and logging mechanisms, writing detailed logs with timestamps to a log file for troubleshooting and monitoring the automation process.
- **Configuration Management**: Loads settings from a configuration file, allowing for flexible program adjustments without altering the code.
- **Screenshot Capture**: Takes screenshots at various stages of the form submission process, providing visual proof of the automation and aiding in debugging.
- **Session Management**: Includes functions to manage browser sessions effectively, ensuring that the web browser is properly closed after the automation tasks are completed.
- **Command Line Execution**: Designed to be run as a standalone script, which can be executed directly from the command line, making it suitable for integration into larger systems or scheduled tasks.

## Methods 

### __init__
This is the constructor for the `FillOutForm` class. It initializes the WebDriver for Selenium, sets up file paths and configuration settings, and defines default values for various attributes used throughout the class.

### connectGoogle
This method sets up the connection to Google's services using OAuth2 credentials, allowing the script to interact with Google Sheets. It handles authentication and logs any errors encountered during the connection process.

### logit
This method is used for logging. It generates a timestamp for each log entry and writes the entry to a log file. This is useful for debugging and tracking the execution of the script over time.

### load_settings
Loads configuration settings from a file named `settings.cfg`. This method reads the file line-by-line, processes each setting, and stores these settings in the class attributes. If the settings file does not exist, it creates one with default settings. It logs all actions, whether loading is successful or encounters errors.

### find_category_value
Searches for a category value in a predefined list of categories based on a given input category type. It returns the corresponding value if the category type is found.

### wait
A simple method that pauses the script for a specified number of seconds. This is often used to ensure that web pages have fully loaded before the script attempts to interact with them.

### navigate
Uses Selenium to open a web browser to a specified URL (stored in `cfg_site`). It logs the navigation action, including any errors if the URL is not provided.

### find_elements
Searches for and stores dynamic form element IDs necessary for login by examining the webpage's DOM. It is specifically looking for elements by their XPATH and updates the internal state with these element IDs.

### find_elements2
Similar to `find_elements`, but tailored for finding and storing form elements related to submitting posts or questions on a form. This method dynamically captures the largest element ID numbers for use in other actions.

### log_in
Attempts to log into a website using credentials and the element IDs found by `find_elements`. It navigates to the login page, inputs user credentials, and submits the login form. It captures screenshots during the login process and logs the outcome.

### getdata
Loads data from either a CSV file or a Google Sheet into the program for processing. It formats this data into a list of dictionaries, where each dictionary represents a row of data from the source.

### run_data
Iterates through the data loaded by `getdata`, logs each entry, and uses this data to fill out and submit forms on the web page by calling other methods like `find_elements2` and `fill_out_form`.

### fill_out_form
Fills out a form on the webpage using the data and element IDs stored from previous methods. It uses JavaScript to insert data into the correct fields and submits the form. It logs each step of the process and captures screenshots of the filled and submitted forms.

### web_quit
Cleans up by closing the Selenium WebDriver session, ensuring that the browser is properly closed after the script’s execution.

