from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
from textblob import TextBlob

# Initialize the WebDriver
driver = webdriver.Chrome()
driver.get('https://www.imdb.com/title/tt13016388/reviews?ref_=tt_ov_rt')

# Click the "Load More" button multiple times
while True:
    try:
        # Wait until the "Load More" button is clickable
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Load More")]'))
        )
        # Scroll to the button
        driver.execute_script("arguments[0].scrollIntoView();", element)
        # Click the button
        element.click()
        print("Clicked 'Load More' button")
        sleep(2)  # Add a small delay to allow the page to load
    except Exception as e:
        print("No more 'Load More' button found or an error occurred:", e)
        break

# Get the page source after all clicks
page_source = driver.page_source
driver.quit()

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")
rev = soup.findAll('div', class_='text show-more__control')

# Extract reviews
movies = [movie.text for movie in rev]

# Create a DataFrame
df_subset = pd.DataFrame()
df_subset['Review'] = movies

# Conduct sentiment analysis
df_subset['Sentiment'] = df_subset['Review'].apply(lambda review: TextBlob(review).sentiment.polarity)

# Print the first few rows of the DataFrame
print(df_subset.head())

# Print the summary of the DataFrame
print(df_subset.info())

# Export the DataFrame to a CSV file
df_subset.to_csv('3_body_reviews_with_sentiment.csv', index=False)

print("DataFrame exported to '3_body_reviews_with_sentiment.csv'")