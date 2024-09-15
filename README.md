
![Screenshot 2024-09-15 020441](https://github.com/user-attachments/assets/d6370ced-58fc-4b6b-a2c1-3725ecde164a)





### The app that finds what is important to you and makes sure you never miss an email again
#### Overview
 - Full stack application with a combination of Next JS and Flask
 - Uses Google and Email API along with Google Cloud Project to retrieve data on the last 5,000 read and unread emails
 - Utilized Clerk authentication to validate emails --> important for making API calls
 - This data is used to fine tune an LLM called **Distill Bert** through Hugging Face's trainer to predict which emails are relevant enough to be read
    - achieved an accuracy of **88 percent** on our test set.
 - Finally use trained LLM to make predictions on if an email is important enough to read

How to run
1. Setup Clerk Authentication
2. Setup Google Project
3. Get Certificates Json
4. Clone Project
5. npm install
6. npm run dev
7. python3 server.py runserver
