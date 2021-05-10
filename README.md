## Shopify Backend Developer Intern Challenge: Image Repo

# Fully Developed Features

- Uploading of images, using `multipart/form-data`
- storing of images, using Django FileSystem
- downloading of previously uploaded images, returned as a binary data stream
- user permissions surrounding images (i.e. only)
- login, signup, and token authentication
- frontend dashboard, UI for uploading image

# Features in Progress

- Market: Image Transaction model already set up; if more time allowed, would have implemented money transfer
- Sharing: Implemented a viewers field in the ImageData model; if more time allowed, would have implemented sharing so that a subset of users can also view images of others

# Testing Instructions

- first create a virtual environment and run `pip install -r requirements.txt`
- then run `python manage.py runserver`, visit `http://localhost:8000` to make an account and test the uploading on frontend
- alternatively, can also run `python test.py` from the root directory to test the uploading and downloading endpoints