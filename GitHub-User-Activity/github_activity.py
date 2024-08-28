import sys
import requests

def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"
    
    try:
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            events = response.json()
            
            # Display recent activities
            if events:
                for event in events[:10]:  # Display the last 10 events
                    event_type = event['type']
                    repo_name = event['repo']['name']
                    
                    if event_type == 'PushEvent':
                        commits = len(event['payload']['commits'])
                        print(f"Pushed {commits} commit(s) to {repo_name}")
                    elif event_type == 'IssuesEvent' and event['payload']['action'] == 'opened':
                        print(f"Opened a new issue in {repo_name}")
                    elif event_type == 'WatchEvent' and event['payload']['action'] == 'started':
                        print(f"Starred {repo_name}")
                    else:
                        print(f"{event_type} in {repo_name}")
            else:
                print("No recent activity found for this user.")
        else:
            print(f"Error: Unable to fetch data for username '{username}'. HTTP Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: An error occurred while fetching data - {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python github_activity.py <github-username>")
        return
    
    username = sys.argv[1]
    fetch_github_activity(username)

if __name__ == "__main__":
    main()
