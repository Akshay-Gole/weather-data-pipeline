# Devlopement Notes

## Step 1: Fetching and saving weather data

### Goal
Fetch Adelaide's hourly forecast and save it a raw_weather.json.

### What I did
- Used request.get() to call the API.
- set timeout=(5, 15)
- called response.raise_for_status() 
- Parsed the response using response.json()
- saved the data using json.dump()

### Why i did it
- a tuple because 5 sec for connection timeout and 15 sec for read timeout
- raise_for_status() lets me handle HTTP error responses
- Saving the raw data lets me inspect and reprocess it later
  without making another API request
- indent=4 makes the saved JSON easier to inspect

### Problem I solved
I learned that HTTP errors and connection errors are different.
An HTTP error means the server returned an error response;
a connection error means communication failed.

### Next step
Inspect the hourly JSON structure and check that the timestamp,
temperature and humidity lists have matching lengths.

## Step 2: Converting hourly data into records

### Goal

Convert the hourly forecast lists into a list of dictionaries, with one dictionary per hour.

### What I did

- Created a function called convert_to_records(data). 
- Extracted time, temperature_2m and relative_humidity_2m from data["hourly"]. 
- Checked that all three lists had matching lengths. 
- Raised a ValueError with the lengths if they did not match. 
- Used a loop to combine values at the same index into a dictionary. 
- Returned the records and printed their count and first two entries outside the function. 
- Tested valid input and deliberately unequal list lengths.

### Why I did it
- Values at the same index describe the same hour. 
- Checking lengths prevents incomplete or silently dropped records. 
- A dictionary gives each value a clear name: timestamp, temperature_c and humidity_pct. 
- Returning the records lets me pass them to the cleaning function later. 
- Using data directly avoids reading the JSON file again because the response is already in memory.

### Problem I solved
- I learned how to combine three separate lists into individual hourly records. 
- I also learned that raising a ValueError stops the function immediately. The calling code can catch that error and display a clear message. 

### Next step

Validate timestamps, temperatures and humidity values, remove duplicate timestamps, and sort the valid records.

## Step 3: Validating, cleaning and saving weather records

### Goal

Validate hourly weather records, remove duplicates, sort valid records by timestamp and save them to a CSV file.

### What I did

- Created helper functions to validate timestamps, temperatures and humidity values.
- Used datetime.strptime() to check timestamps against %Y-%m-%dT%H:%M. 
- Checked that temperatures were not missing and were numeric. 
- Checked that humidity values were numeric and between 0 and 100. 
- Created clean_records(records) to separate kept, rejected and duplicate records. 
- Used a set to track accepted timestamps and keep the first valid record for each timestamp. 
- Sorted the kept records chronologically. 
- Applied the cleaning function to the actual API records and printed the three counts. 
- Created create_record_csv() using csv.DictWriter. 
- Saved the kept records to cleaned_weather.csv with a header row.

### Why I did it
- Invalid values could produce incorrect daily summaries. 
- Duplicate records could give some hours extra weight when calculating averages. 
- Validating before checking duplicates prevents an invalid record from blocking a later valid record with the same timestamp. 
- Sorting makes the cleaned data easier to inspect and use. 
- CSV provides a table format that can be opened in spreadsheet applications or loaded into a database later. 
- Keeping CSV writing in a separate function allows me to reuse it for daily summaries.

### Problem I solved

- I combined validation, duplicate removal and sorting into a cleaning function, then saved its valid output as a CSV file.

- I also kept rejected and duplicate records separately so I can inspect them and understand what was removed.

### Next step
Group the cleaned records by date, calculate daily statistics and save them to daily_summary.csv.