# Data_Science_Practicum_II - Regis University, Denver Colorado

MSDS692: Data Science Practicum

Author: Brad Eland

Spring 2025
![image](https://github.com/user-attachments/assets/b1b6fba2-8339-4c5c-836c-a843d1bf879d)


# 🔍 LinkedIn Experience Scraper
Have you ever had to do the laborius task of going out and finding various pieces of employment information? If so, here's an excellent tool to help save time and money. LinkedIn does change up their format from time to time, so it may work for now and break in the future.
Do be careful and know the rules and regulations for scraping this data in your area. 
A Python-based tool to extract key details from the **Experience** section of public LinkedIn profiles. This project was built to help students and researchers save time manually gathering employment data. Thus, they can work on things to better their campus with freed up time!

## ✨ Features

- Extracts structured data from the Experience section of LinkedIn profiles
- Supports scraping multiple profiles in a loop
- Randomized delays to reduce risk of being flagged-I would try like a minute or two random sleeps!
- Saves output as `.csv` for easy analysis
- Has a section where you can QA your results and iterate between 2 tabs in a browser

## 📌 What It Extracts

From the most recent or all listed jobs:
- ✅ Job Title
- ✅ Company Name
- ✅ Employment Type (Full-time, Part-time, Internship, etc.)
- ✅ Employed or assumption of not employed if "present" is not in the first record of the experience
- ✅ LinkedIn URL for the person
- ✅ Location of the person being seearched (City, State)

## ⚙️ Requirements

- Python 3.9+
- Google Chrome + ChromeDriver (Installed on your project!) as shown below:
![image](https://github.com/user-attachments/assets/6c7305e6-306b-474c-a4c8-940123b5b895)

- Gmail for sending the email to various recipients
- Packages:
  - `selenium`
  - `beautifulsoup4`
  - `pandas`
  - `time`, `random`
  - `email.message`
  - `dotenv`
  - `csv`
  - `smtplib`
  - Names of people along with a university or some other attribute shared between everybody

# Data Cleaning
Given the dynamic nature of how LinkedIn is set-up, this wasn't so much about cleaning the data, but figuring out how to get the most people brought through as possible! In the end there are many loops and iterations. I believe LinkedIn had 3-4 levels of how people would be found even after using the person's name along with "AND Regis University."
Following finding the person, I then had to iterate through I believe 3 variations of what the **Experience** would have as far as where to gather the information listed in the **What It Extracts** section mentioned above. 

# Results:
In the end before LinkedIn found me out as a "bot" were ok.  I was able to iterate through 166 records (could've been more possibly with longer/more sleeps). Of those 166 records, there were 66 blank. This is typically due to not finding a person.
![image](https://github.com/user-attachments/assets/f34a88ee-fdb4-4f77-b48c-14b926a80810)


I then wrote a script to make it easier on the people if they can find the LinkedIn URL for various people.  I looked at those 76 of those results and found that 48 were found (close to the same percentage as overall). Of the 48 that were found, only one was "incorrect." LinkedIn tries to assist as much as possible at finding somebody, which can be good or bad. The person that was "incorrect," was close to the person searched, but they just taught at a school with, "St. Regis School." Still, not too bad to have ~98 accuracy (I know over a smaller sample size)!
![image](https://github.com/user-attachments/assets/16676e07-e2b4-4c88-9250-c2c7e11e69ae)

If I would've known the results for every person and how their job history would be pulled, I could've written one section a little better. That section being where it gets the company name. Based on me iterating through the first 10 or so records and methodically working through the dynamic nature of LinkedIn I could've gathered the company name better. Further down in my results after I let my process run without intervention (the end goal), there were more "full-time" records for the company/title.  It was difficult working through each iteration and carrying it through and since there are so many ways data can process, this is a difficult task without knowing in the beginning. If I wouldn't have been detected after letting it run once, after I had iterated through so many variations, I know I could've gotten the correct results. The nice thing about my thoughts after were to be able to QA based on the LinkedIn URL for each person. This would allow for gathering the requisite data pretty easily. Since this ended up being a proof of concept, it went ok. However, if I had created a couple dummy accounts, I would've tested to see just the blank records that came through (to see if I could gather more people), as well as some of the people that had "full-time" because I thought I had captured most locations of where they could be. Dynamic content for scraping can be refined even greater per platform. 

# Email Sends of results
In the end you can send a person an email with the attached .csv. This is done using the `smtplib` mentioned in the **Requirements** section above. You need to have access to gmail or any other instance that allows smtplib sends. The hashing of the email password is pretty simple and I included what to search for in the python script attached to this project.

# Thoughts on what could be improved or other possible solutions
Overall, the use of intermarket analysis can and should be used when trying to determine even one stock.  The reason for this is how closely related things can be.  If one thing happens to another stock it can greatly affect the outcome of the other.  If I could continue my research I would do the following:

•	Use an API (which I’ve used for various other projects but, I wanted to stretch). These still may not provide what was wanted or needed

• Maybe could’ve put longer sleeps than random between 5 to 15 seconds so it may not have detected

• If I really needed this for research and to go faster, it may be worth creating 7-10 dummy accounts and doing batches if LinkedIn could detect bots with even longer random sleeps

