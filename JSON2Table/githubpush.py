from git import Repo

# Specify your GitHub repository URL
repo_url = 'https://github.com/aanpala/StockData.git'

# Clone the repository (if it doesn't exist locally)
repo = Repo.clone_from(repo_url, '/path/to/local/repo')

# Make changes to the repository

# Commit your changes
repo.index.add(['dummy', 'file2.txt'])
repo.index.commit('Your commit message')

# Push the changes to GitHub
origin = repo.remote(name='origin')
origin.push()