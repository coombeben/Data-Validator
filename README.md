# dogSelector
A webapp hosted on Azure and powered by Flask, created to enable friends and family to easily contribute to my dissertation data collection.

The process:
1) A SQL database is populated with dog breeds and a corresponding query to get photos of that breed
2) A Python script calls the Google/Bing Images API for each breed and populates the database with image URLs
3) When a user visits the site, they are presented with a breed name and 10 images. The users mark the vaild images and press "Submit"
4) (In)valid image URLs are marked as such in the database, according to the user's input
5) (At a later point) All valid images are automatically downloaded, resized, and agressively de-dupliciated for training a machine learning model

Overall, more than 60,000 dog images were collected in this fashion

Python | Flask | SQL Sever | Azure
