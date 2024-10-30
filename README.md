# README.md

- Data was collected from the *GitHub API* for users in **Barcelona with over 100 followers**, extracting details about their profiles and repositories.
- One interesting finding was that **"JavaScript"** is the most popular language, but **"Vim Script"** has the highest average number of stars per repository.
- Developers could enhance visibility by **optimizing repository settings** and focusing on languages that gather high engagement.

## Project Overview

This project involves scraping user and repository data from GitHub to understand trends among top-followed developers in Barcelona. Key metrics include follower counts, programming languages used, and account creation dates.

### Data Collection Process

Using the GitHub API, users were filtered based on location (Barcelona) and follower count (over 100), with additional details retrieved per user. Repository information, including star counts, language usage, and license types, was also gathered.

### Analysis Highlights

1. **Top Languages**: JavaScript was the most popular, followed by Python, but repositories in Vim Script had the highest average stars.
2. **Popular Licenses**: The MIT license is most commonly used, followed by Apache-2.0 and "Other" licenses.
3. **User Trends**: Freelancing was the most frequently listed work setting, highlighting a trend towards independent work among top GitHub users in Barcelona.

### Recommendations

- **For Developers**: Emphasizing quality and focus in selected languages, such as Vim Script and JavaScript, could attract more stars and followers.
- **For GitHub Optimizations**: Ensuring repositories have useful information in bios, README files, and enabling features like Wiki and Projects may enhance engagement.

## Files

- `users.csv`: Contains profile details of each user.
- `repositories.csv`: Contains detailed information on each user's repositories.
