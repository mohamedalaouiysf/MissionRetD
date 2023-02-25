import time
import csv
from github import Github

#token github
gitInstance = Github("***********************************")

commitKeywords= ['RGPD','GDPR','vie privee']
def getLen(keyword):
    results = gitInstance.search_repositories(keyword)
    print(results.totalCount)

def getUrlsByName(keyword):
    results = gitInstance.search_repositories("{} stars:>10".format(keyword))
    results = sorted(results, key=lambda x: x.stargazers_count, reverse=True)
    with open(keyword+'.csv', mode='w',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["NAME","URL"])
        for repo in results:
            writer.writerow([repo.name,repo.html_url])
        

def getUrlsByCommits(keyword):
    results = gitInstance.search_commits("{}".format(keyword)) 
    with open(keyword+'_commit.csv', mode='w',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["NAME","URL"])
        for commit in results:
            link = "/".join(commit.html_url.split('/')[:5])
            name = link.split("/")[-1]
            writer.writerow([name,link])


def getUrlsByTicket(keyword):
    results = gitInstance.search_issues("RGPD")
    with open(keyword+'_ticket.csv', mode='w',newline='') as file:    
        writer = csv.writer(file)
        writer.writerow(["NAME","URL"])
        for issue in results:
            link = "/".join(issue.html_url.split('/')[:5])
            name = link.split("/")[-1]
            writer.writerow([name,link])


getUrlsByTicket('GDPR')
