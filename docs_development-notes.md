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

## Step 2: Inspecting the hourly JSON