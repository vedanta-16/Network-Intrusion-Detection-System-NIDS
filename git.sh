#!/bin/bash
# 1. Initialize git in your project folder (if you haven't already)  
git init

# 2. Add all your local files to the staging area
git add .

# 3. Commit your changes with a descriptive message
git commit -m

# 4. Link your local project to the browser-based repository URL you copied
git remote add origin https://github.com/vedanta-16/Network-Intrusion-Detection-System-NIDS-

# 5. Push your code to the remote server
git push -u origin main


