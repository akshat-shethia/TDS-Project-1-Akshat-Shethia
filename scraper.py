import requests
import csv
import time

# GitHub API token
GITHUB_TOKEN = 'Enter Your Github Token here'
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}



# Helper function to clean up company names
def clean_company_name(company):
    if company:
        company = company.strip().lstrip('@').upper()
    return company



# Function to fetch users from the GitHub API
def fetch_users(city="Barcelona", min_followers=100):
    users = []
    page = 1

    while True:
        url = f"https://api.github.com/search/users?q=location:{city}+followers:>{min_followers}&page={page}&per_page=100"
        response = requests.get(url, headers=HEADERS)
        data = response.json()

        # Break if no more results
        if 'items' not in data or not data['items']:
            break

        for user in data['items']:
            # Get full user info
            user_url = user['url']
            user_response = requests.get(user_url, headers=HEADERS)
            user_data = user_response.json()

            # Extract required fields
            users.append({
                'login': user_data['login'],
                'name': user_data['name'] or '',
                'company': clean_company_name(user_data['company']) or '',
                'location': user_data['location'] or '',
                'email': user_data['email'] or '',
                'hireable': user_data['hireable'] or False,
                'bio': user_data['bio'] or '',
                'public_repos': user_data['public_repos'],
                'followers': user_data['followers'],
                'following': user_data['following'],
                'created_at': user_data['created_at'],
            })
        page += 1
        time.sleep(1)  # Avoid hitting API rate limits

    return users



# Function to fetch repositories for a user
def fetch_repositories(user_login):
    repositories = []
    page = 1

    while True:
        url = f"https://api.github.com/users/{user_login}/repos?per_page=100&page={page}"
        response = requests.get(url, headers=HEADERS)
        repo_data = response.json()

        # Break if no more repositories
        if not repo_data:
            break

        for repo in repo_data:
            repositories.append({
                'login': user_login,
                'full_name': repo['full_name'],
                'created_at': repo['created_at'],
                'stargazers_count': repo['stargazers_count'],
                'watchers_count': repo['watchers_count'],
                'language': repo['language'] or '',
                'has_projects': repo['has_projects'],
                'has_wiki': repo['has_wiki'],
                'license_name': repo['license']['key'] if repo['license'] else '',
            })

        # If fewer than 100 repositories are returned, it means we're on the last page
        if len(repo_data) < 100:
            break

        page += 1  # Move to the next pag
        time.sleep(1)  # Avoid hitting API rate limits

    return repositories


# Save users to CSV
def save_users_to_csv(users, filename="users.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=users[0].keys())
        writer.writeheader()
        writer.writerows(users)
        
        

# Save repositories to CSV
def save_repositories_to_csv(repositories, filename="repositories.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=repositories[0].keys())
        writer.writeheader()
        writer.writerows(repositories)
        
        

def main():
    print("Fetching users...")
    users = fetch_users()
    save_users_to_csv(users)
    print(f"Saved {len(users)} users to users.csv")

    uniq_users = len({user["login"]: user for user in users}.keys())   # Sanity check
    print(f"Found {uniq_users} unique users")

    total_expected_repos = sum(user["public_repos"] for user in users)
    print(f"Expected to fetch {total_expected_repos} repositories...")

    print("Fetching repositories...")
    all_repositories = []
    for user in users:
        user_repos = fetch_repositories(user["login"])
        all_repositories.extend(user_repos)
        print(f"Fetched {len(user_repos)} repositories for user {user['login']}")

    save_repositories_to_csv(all_repositories)
    print(f"Saved {len(all_repositories)} repositories to repositories.csv")

    print('Repos pass sanity check:', total_expected_repos == len(all_repositories))
    
    

if __name__ == "__main__":
    main()