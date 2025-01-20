from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
import pandas as pd
import time

# Initialize WebDriver for Microsoft Edge
edge_driver_path = r"C:\Users\sayus\Downloads\edgedriver_win64\msedgedriver.exe"  # Path to Microsoft Edge WebDriver
options = webdriver.EdgeOptions()
service = Service(edge_driver_path)

driver = webdriver.Edge(service=service, options=options)

# Base URL for scraping
base_url = "https://www.visualcrossing.com/weather/weather-data-services/Nagpur/metric"

# Date range
start_year = 2020
end_year = 2024
data = []

# Iterate through each week
for year in range(start_year, end_year + 1):
    for month in range(1, 13):  # Months 1 to 12
        for day in range(1, 32, 7):  # Weekly increments
            start_date = f"{year}-{month:02d}-{day:02d}"
            end_date = f"{year}-{month:02d}-{min(day + 6, 31):02d}"
            url = f"{base_url}/{start_date}/{end_date}"
            
            # Open URL
            driver.get(url)
            time.sleep(3)  # Wait for page to load
            
            # Handle modal box if present
            try:
                close_button = driver.find_element(By.CLASS_NAME, "btn-close")  # Locate the close button
                close_button.click()  # Close the modal
                time.sleep(2)  # Wait for modal to close
            except Exception as e:
                print(f"No modal found for {start_date} to {end_date}: {e}")
            
            # Scrape table data
            try:
                # Find table
                table = driver.find_element(By.CLASS_NAME, "table-responsive")
                rows = table.find_elements(By.TAG_NAME, "tr")
                
                # Extract header
                # Extract header
                if not data:  # Only once
                    headers = [th.text for th in rows[0].find_elements(By.TAG_NAME, "th")]
                    data.append(headers)

                # Extract row data
                for row in rows[1:]:  # Skip header row
                    cells = row.find_elements(By.TAG_NAME, "td")
                    row_data = [cell.text for cell in cells]
                    if len(row_data) < len(headers):  # Pad with empty strings if columns are less
                        row_data.extend([''] * (len(headers) - len(row_data)))
                    elif len(row_data) > len(headers):  # Trim if columns are more
                        row_data = row_data[:len(headers)]
                    data.append(row_data)

            except Exception as e:
                    print(f"Error scraping {start_date} to {end_date}: {e}")
                    continue

# Close the driver
driver.quit()

# Save to CSV
df = pd.DataFrame(data[1:], columns=data[0])  # Exclude header row
df.to_csv("nagpur_weather.csv", index=False)
print("Data saved to 'nagpur_weather.csv'")
