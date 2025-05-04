"""
Original Developer: Brad Eland
Class: MSDS Practicum II Regis University
Class Dates: March 2025-May 4th, 2025
One would normally get the list then load entirely vs. appending each record.  However, I wrote it this way so that I could restart if one record failed! Have to save as utf-8 if want to use the links!
"""

import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import csv

from bs4 import BeautifulSoup
import time
import random
import smtplib

from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

# can modify this to be logner sleeps and maybe the program won't think you're a bot!
sleep_time = random.uniform(7, 15)
time.sleep(sleep_time)


desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
# todo: modify this filename to whatever you have your .csv saved as!
v_file_name ='MSDS_Grads_for_project_testing.csv'
v_file_path = os.path.join(desktop_path, v_file_name)
v_file_name_2 = 'MSDS_Grads_2023_with_vals.csv'
v_file_path_2 = os.path.join(desktop_path, v_file_name_2)
v_file_name ='YEP.txt'
v_file_path_3 = os.path.join(desktop_path, v_file_name)


def main():
    # TODO: set this up for at least an idea of what can be done to not have UN/PW hardcoded! You can have a .txt/.csv document or PW manager location you API into. Skip this or hardcode the variable in the locations that are the variables within the definitions!
    v_no_touch = read_csv(v_file_path_3)
    v_user_platform = v_no_touch.iloc[0]
    v_user_platform_final = v_user_platform[0]
    v_pass_platform = v_no_touch.iloc[1]
    v_pass_platform_final = v_pass_platform[0]
    v_user_send_email = v_no_touch.iloc[2]
    v_user_send_email_final = v_user_send_email[0]
    v_pass_send_email = v_no_touch.iloc[3]
    v_pass_send_email_final = v_pass_send_email[0]
    # Todo: you need to have whatever path successfully set-up/in the proper location. Mine is currently just my desktop. If you have a server path (probably more secure), use that.
    # Todo: Filename can be set to whatever, just make sure you have that up top. Make sure to use the correct formatting.
    v_list_to_pass = read_csv(v_file_path)
    v_driver = d_get_driver(v_user_platform_final, v_pass_platform_final, url='https://www.linkedin.com/login')
    d_scrape_linkedin_profile(v_driver, v_list_to_pass)
    # # this sets the header rows after the file has completely loaded! :)  Since it was appending, again because couldn't be certain would run w/out error, it didn't just get inserted 1x.
    d_add_header_rows(v_file_path_2)
    # this sets up the email send. It's pretty simple from what I've seen to create a hashed password (I'd recommend storing in a place like AWS secrets manager). I'm happy to set one up. They're .40 cents per secret per month! I'd recommend this for any code where a UN/PW is required!
    d_send_email(v_user_send_email_final, v_pass_send_email_final, v_file_path_2)
    # ******************************************************************* bonus for QAing purposes! I ran through about 75 people in 15 minutes checking values from the .csv file*******************************************************************
    # todo: if you have all the links in the .csv and have it stored to the filepath 2 location (you can set-up wherever!), this will open a tab for each record! File needs to be created first in steps above or you can just create with any values.
    v_list_pass_links = read_csv(v_file_path_2)
    d_open_multiple_tabs(v_list_pass_links)


def read_csv(v_file_path):
    v_data = pd.read_csv(v_file_path)
    df_final_no_nan = v_data.fillna('')
    return df_final_no_nan


# I went through 70 on the list of people that I got! There was one person that had "ST. Regis Almasa Capital" as their workplace and their name was close to what was in the list so it pulled them through.
# I was able to find people that may not show they attended Regis as a college, but it was mentioned in their profile.  Again, linkedin trying to be as helpful as it can!
def d_open_multiple_tabs(v_list_to_iterate):
    # some values came through as tab separated. One of them being the URL for linkedin profile.  Therefore, used this instead of cleaning at the DF level.
    v_link_to_pass = v_list_to_iterate['\tLinkedIn URL']
    # Initialize the WebDriver (replace with your browser driver)
    driver = webdriver.Chrome()  # or webdriver.Firefox(), etc.

    # Open a new tab using JavaScript
    driver.execute_script("window.open();")
    for v in v_link_to_pass:
        if v == '':
            pass
        else:
            # Switch to the new tab
            current_window = driver.current_window_handle
            all_windows = driver.window_handles
            for window in all_windows:
                if window != current_window:
                    driver.switch_to.window(window)
                    break

            # Navigate to a URL in the new tab
            driver.get(f'{v}')

    # Close the browser (optional)
    driver.quit()


# this definition adds a header row in the end!
def d_add_header_rows(v_file_path_to_write):
    try:
        with open(v_file_path_to_write, 'r') as file:
            lines = file.readlines()
        # couldn't test this. I know
        if lines[000] == '\n':
            del lines[000]
    except FileNotFoundError as m:
        print(m)
        return
    lines.insert(0, header + '\n')
    # make sure use utf-8 encoding! Python/Pandas LOVE reading in utf-8 for .csv :)
    with open(v_file_path_to_write, 'w', encoding='utf-8') as file:
        file.writelines(lines)

# header rows to insert. You can create whatever you want/need them to be in whatever order. These were the ones that were provided and their order.
header = 'FirstName, LastName, School Email, Recipient Primary Major, Recipient Education Level, Recipient Graduation Date,	Employed, Employer Name, Employer Industry,	Job Title, 	Employment Type FT or PT,	City/State,	LinkedIn URL'


# this definition is what sends the file via email. You of course can attach to an email you create if you'd like. My plan was based on this being an ongoing project so each time it ran, you'd just send the email!
# I do know how to set-up to run as often as you'd like w/task scheduler, but the product owner said this is a 1x thing :(  So, I didn't pursue this. Happy to help anybody set this up if it's ongoing!
def d_send_email(user, pw, v_pass_file):
    # Gmail credentials
    # It's pretty easy to set up the hashed password! I'm redacting mine, but happy to share how to do this!
    # I followed this AI overview to get mine working: https://www.google.com/search?q=setting+up+hashed+password+for+gmail+sends+emails&rlz=1C1GCEA_enUS941US941&oq=setting+up+hashed+password+for+gmail+sends&gs_lcrp=EgZjaHJvbWUqBwgBECEYoAEyBggAEEUYOTIHCAEQIRigATIHCAIQIRigATIHCAMQIRigAdIBCTE2MDc4ajBqN6gCCLACAfEFOXybp7TJJas&sourceid=chrome&ie=UTF-8
    GMAIL_USER = f'{user}'
    GMAIL_PASSWORD = f'{pw}'

    # Email details
    TO_EMAIL = "brad.eland@gmail.com"
    SUBJECT = "CSV File Attachment"
    BODY = "Hello,\n\nPlease find the attached CSV file.\n\nBest regards."

    # File to attach
    CSV_FILE_PATH = f'{v_pass_file}'

    # Create email message
    msg = EmailMessage()
    msg["From"] = GMAIL_USER
    msg["To"] = TO_EMAIL
    msg["Subject"] = SUBJECT
    msg.set_content(BODY)

    # Attach CSV file. You can modify to various subtypes, but I prefer .csv.
    if os.path.exists(CSV_FILE_PATH):
        with open(CSV_FILE_PATH, "rb") as file:
            msg.add_attachment(file.read(), maintype="text", subtype="csv", filename=os.path.basename(CSV_FILE_PATH))
    else:
        print("CSV file not found!")
        exit()

    # Send email via SMTP
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)


def d_get_driver(user, pw, url):
    # you can store UN/PW in a secure location like AWS and call from there!
    v_username = f'{user}'
    v_password = f'{pw}'
    # todo: here's where you can get most recent version of chrome driver.  You'll need to see where this is by going to your chrome version. I can help folks find this. https://googlechromelabs.github.io/chrome-for-testing/#stable
    # calling .exe (installed in the python project for ease of use. Can path anywhere your project is housed!)
    service = Service(executable_path='chromedriver.exe')
    # instantiates the google chrome website
    driver = webdriver.Chrome(service=service)
    # takes you to whatever URL you've posted. In this case, doing linkedin
    driver.get(f'{url}')

    # Find username and password fields and log in
    email_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")

    email_field.send_keys(v_username)
    password_field.send_keys(v_password)
    password_field.send_keys(Keys.RETURN)  # Hit 'Enter' after entering password

    # TODO: break here for solving security check IF YOU'VE RUN THIS MANY TIMES IN A DAY!!

    # Wait for the page to load after login
    time.sleep(sleep_time)

    return driver


def d_scrape_linkedin_profile(driver, v_list_pass):
    # how to handle if multiple names like "Kayla Smith" or things that are "common?" :(
    try:
        # todo: must have 3-5 second sleeps (OR GREATER) or the script moves too fast and will break!
        # this uses the .iterrows to iterate through each row. Since there is no DB/fields these will insert into, keeping headers without _, camelcase.
        # Usually, depending on the use, you'd want to not have spaces in headers.
        for index, row in v_list_pass.iterrows():
            print(f'this is the {index} number!')
            v_fn = row['FirstName']
            v_ln = row['LastName']
            v_search_name = f'{v_fn} {v_ln}'

            # for testing!
            # print(f'{v_fn} {v_ln}')
            # Locate the search bar
            search_bar = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'Search')]")

            # Clear the search bar and enter the name
            search_bar.clear()

            # Inputs User searching for! There were I think 3 iterations I had clicking buttons etc. . . Ended up finding how to do it this way :)
            # FANCY DOESN'T ALWAYS EQUAL BETTER!  I could find and automate many errors! Since we are looking for specifically "Regis University," This way is the best upon multiple variations :)
            search_bar.send_keys(f'{v_search_name} AND Regis University')
            time.sleep(sleep_time)
            search_bar.send_keys(Keys.RETURN)  # Hit 'Enter' after entering user searching for
            time.sleep(sleep_time)  # Wait for results to load
            # set try except lower because I knew it would be able to get the initial stuff. Needed to be able to get if couldn't find or had a question!
            try:
                print(index)
                v_top_record = search_bar.find_element(By.XPATH, "/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[1]/div/ul/li/div/div/div/div[1]/div[1]/div/div/span[1]/span/a/span/span[1]")
                time.sleep(sleep_time)
                v_top_record.click()
                time.sleep(sleep_time)
                v_records_returned = d_start_scraping(driver, search_bar)
                # Set all values from column 'employer name' onward in row 1
                v_list_pass.loc[index, "Employed":] = v_records_returned
                row = v_list_pass.iloc[index]
                v_to_csv_list = []
                for v in row:
                    v_to_csv_list.append(v)
                d_start_writing(v_to_csv_list)
            except Exception as e:
                v_issue = str(e)
                try:
                    if 'Message: no such element: Unable to locate element: ' in v_issue:
                        v_top_record = search_bar.find_element(By.XPATH, '/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[1]/div/ul[2]/li[1]/div/div/div/div[2]/div/div[1]/div/span[1]/span/a/span/span[1]')
                        v_top_record.click()
                        time.sleep(sleep_time)
                        v_records_returned = d_start_scraping(driver, search_bar)
                        # Set all values from column 'age' onward in row 1
                        v_row_to_write = v_list_pass.loc[index, "Employed":] = v_records_returned
                        v_row_to_write_as_list = v_list_pass.iloc[index].tolist()
                        v_to_csv_list = []
                        for v in v_row_to_write_as_list:
                            v_to_csv_list.append(v)
                        d_start_writing(v_to_csv_list)
                        continue
                    else:
                        pass
                except Exception as e4:
                    v_issue = str(e4)
                try:
                    if 'Message: no such element: Unable to locate element: ' in v_issue:
                        v_top_record = search_bar.find_element(By.XPATH, '/html/body/div[6]/div[3]/div[2]/div/div[1]/main/div/div/div[1]/div/ul[2]/li/div/div/div/div[2]/div[1]/div[1]/div/span[1]/span/a/span/span[1]')
                        v_top_record.click()
                        time.sleep(sleep_time)
                        v_records_returned = d_start_scraping(driver, search_bar)
                        # Set all values from column 'age' onward in row 1
                        v_row_to_write = v_list_pass.loc[index, "Employed":] = v_records_returned
                        v_row_to_write_as_list = v_list_pass.iloc[index].tolist()
                        v_to_csv_list = []
                        for v in v_row_to_write_as_list:
                            v_to_csv_list.append(v)
                        d_start_writing(v_to_csv_list)
                        continue
                    else:
                        pass
                except Exception as e3:
                    v_issue = str(e3)
                try:
                    if 'Message: no such element: Unable to locate element: ' in v_issue:
                        v_top_record = search_bar.find_element(By.XPATH, '/html/body/div[5]/div[3]/div[2]/div/div[1]/main/div/div/div[1]/div/ul/li/div/div/div/div[1]/div[1]/div/div/span[1]/span/a/span/span[1]')
                        v_top_record.click()
                        time.sleep(sleep_time)
                        v_records_returned = d_start_scraping(driver, search_bar)
                        # Set all values from column 'age' onward in row 1
                        v_row_to_write = v_list_pass.loc[index, "Employed":] = v_records_returned
                        v_row_to_write_as_list = v_list_pass.iloc[index].tolist()
                        v_to_csv_list = []
                        for v in v_row_to_write_as_list:
                            v_to_csv_list.append(v)
                        d_start_writing(v_to_csv_list)
                        continue
                    else:
                        pass
                except Exception as e5:
                    # had to add in case no results!
                    if search_bar.text == '':
                        v_row_to_write = v_list_pass.iloc[index]
                        v_to_csv_list = []
                        for v in v_row_to_write:
                            v_to_csv_list.append(v)
                        d_start_writing(v_to_csv_list)
                        continue
                    else:
                        print(e3)
                else:
                    print(e)
    except Exception as e2:
        print(e2)


def d_start_writing(v_write):
    v_file_name_write = 'MSDS_Grads_2023_with_vals.csv'
    v_file_path_w = os.path.join(desktop_path, v_file_name_write)
    try:
        with open(v_file_path_w, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(v_write)
    except Exception as e:
        print(f"An error occurred: {e}")


def d_start_scraping(driver):
    # todo: https://www.google.com/search?q=scraping+the+experience+section+of+linkedin+using+selenium+and+beautiful+soup&rlz=1C1GCEA_enUS941US941&oq=scraping+the+experience+section+of+linkedin+using+selenium+and+beautiful+soup&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCTI1NTg5ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8#fpstate=ive&vld=cid:2fb1c01f,vid:SQtwhuYJk3M,st:0
    v_linkedin_url = driver.current_url
    # used for testing with > 1 job
    # v_linkedin_url = 'https://www.linkedin.com/in/brad-eland/'
    # --- STEP 2: Navigate to the LinkedIn profile URL ---
    profile_url = f"{v_linkedin_url}"
    # this takes you directly back to the beginning with the correct URL! :)
    driver.get(profile_url)
    time.sleep(sleep_time)

    # --- STEP 3: Extract the experience section ---
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # --- Get location (city/state) ---
    location_tag = soup.find("span", class_="text-body-small inline t-black--light break-words")
    location = location_tag.get_text(strip=True) if location_tag else "N/A"

    # Grab the job card (most recent experience)
    try:
        v_completed_list = []
        # This selects the first Experience card using its heading
        experience_cards = driver.find_elements(By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section[4]/div[2]/div/div/div/h2/span[1]")
        if experience_cards:
            most_recent = experience_cards[0]
            if most_recent.text == 'About':
                jobs = driver.find_elements(By.CSS_SELECTOR, 'section:has(#experience)>div>ul>li')
                # Set-up counter so it would only iterate 1x (all we need for this project). Had to do a for loop to iterate through web elements.
                counter2 = 0
                for job in jobs:
                    if counter2 > 0:
                        pass
                    else:
                        text = job.text
                        lines = text.splitlines()
                        if lines[8] != '':
                            if 'present' in str.lower(lines[8]):
                                v_employment = 'employed'
                        else:
                            v_employment = 'unknown'
                        if lines[0] != '':
                            v_company = lines[0]
                            # most common things somebody can be as far as job status!
                            search_list = ["full-time", "part-time", "internship", "freelance", "contract"]
                            v_status = 'unknown'
                            v_check = lines[6]
                            for y in search_list:
                                if y == str.lower(v_check):
                                    v_status = y
                                    break
                        else:
                            v_status = 'unknown'
                            v_company = 'unknown'
                        if lines[4] != '':
                            v_job_title = lines[4]
                        else:
                            v_job_title = 'N/A'
                    counter2 += 1
                    v_completed_list = [v_employment, v_company, '', v_job_title, v_status, location, v_linkedin_url]
                    return v_completed_list
            elif most_recent.text == 'Experience':
                # made a for loop to find first job status type. Also, made the value all lower since python looks at string literals.
                if most_recent.text == 'Experience':
                    v_title = driver.find_elements(By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section[4]/div[3]/ul/li[1]/div/div[2]/div[1]/a/div/div/div/div/span[1]")
                    v_title_final = v_title[0].text
                    v_employment = driver.find_elements(By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section[4]/div[3]/ul/li[1]/div/div[2]/div[1]/a/span[2]/span[1]")
                    v_employment = v_employment[0].text
                    if 'present' in str.lower(v_employment):
                        v_employment = 'Employed'
                    else:
                        v_employment = 'unknown-shows work history in the past'
                    try:
                        v_status = driver.find_elements(By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section[6]/div[3]/ul/li[1]/div/div[2]/div[2]/ul/li[1]/div/div[2]/div[1]/a/span[1]/span[1]")
                        v_status_final = v_status[0].text
                    except Exception as f:
                        if str(v_status) == f"[]":
                            v_status = driver.find_elements(By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section[4]/div[3]/ul/li[1]/div/div[2]/div/a/span[1]/span[1]")
                            v_status_final = v_status[0].text
                            search_list = ["full-time", "part-time", "internship", "freelance", "contract"]
                            v_check = v_status_final
                            for y in search_list:
                                if y in str.lower(v_check):
                                    v_status_final = y
                                    break
                        else:
                            v_status_final = 'unknown'

                else:
                    v_title_final = 'unknown'
                    v_status_final = 'unknown'
                if most_recent.text == 'Experience':
                    v_company = driver.find_elements(By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section[4]/div[3]/ul/li[1]/div/div[2]/div[1]/a/span[1]/span[1]")
                    v_company_final = v_company[0].text
                    v_value_to_parse = '·'
                    ind = v_company_final.find(v_value_to_parse)
                    if ind != -1:
                        left_part = v_company_final[:ind]
                        if left_part:
                            v_company_final = left_part
                    else:
                        v_company_final
                else:
                    v_company_final = 'unknown'
                v_completed_list = [v_employment, v_company_final, '', v_title_final, v_status_final, location, v_linkedin_url]
                return v_completed_list
            elif most_recent.text == 'Activity':
                if most_recent.text == 'Activity':
                    v_title = driver.find_elements(By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section[5]/div[3]/ul/li[1]/div/div[2]/div[1]/a/div/div/div/div/span[1]")
                    v_title_final = v_title[0].text
                    v_employment = driver.find_elements(By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section[5]/div[3]/ul/li[1]/div/div[2]/div[1]/a/span[2]/span[1]")
                    v_employment = v_employment[0].text
                    if 'present' in str.lower(v_employment):
                        v_employment = 'Employed'
                    else:
                        v_employment = 'unknown-shows work history in the past'
                        v_status_final = 'unknown - shows work in past'
                    search_list = ["full-time", "part-time", "internship", "freelance", "contract"]
                    v_check = driver.find_elements(By.XPATH, "/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section[5]/div[3]/ul/li[1]/div/div[2]/div[1]/a/span[1]/span[1]")
                    if str(v_check) == '[]':
                        v_check = driver.find_elements(By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section[5]/div[3]/ul/li[1]/div/div[2]/div[1]/a/span[1]/span[1]")
                    elif str(v_check) == '[]':
                        pass
                    else:
                        v_check_name = v_check[0].text

                    if str(v_check) != '[]':
                        v_check_name = v_check[0].text
                        for y in search_list:
                            if y in str.lower(v_check_name):
                                v_status_final = y
                                break
                            else:
                                v_status_final = 'unknown'
                    else:
                        pass
                else:
                    v_title_final = 'unknown'
                if most_recent.text == 'Activity':
                    v_company = driver.find_elements(By.XPATH, "//*[@id='profile-content']/div/div[2]/div/div/main/section[5]/div[3]/ul/li[1]/div/div[2]/div[1]/a/span[1]/span[1]")
                    v_company_final = v_company[0].text
                    v_value_to_parse = '·'
                    ind = v_company_final.find(v_value_to_parse)
                    if v_employment != 'Employed':
                        v_most_recent = 'most recent '
                    else:
                        v_most_recent = ''
                    if ind != -1:
                        left_part = v_company_final[:ind]

                        if left_part:
                            v_company_final = f'{v_most_recent}{left_part}'
                    else:
                        v_company_final
                else:
                    v_company_final = 'unknown'
                v_completed_list = [v_employment, v_company_final, '', v_title_final, v_status_final, location, v_linkedin_url]
                return v_completed_list
    except Exception as e:
        print(e)

# todo: this was going to be the last part! I couldn't test/know where to put because I never got it to complete w/out thinking this program was a bot!
            # Close the WebDriver
            # driver.quit()


if __name__ == "__main__":
    main()
