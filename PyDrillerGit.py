import pandas as pd
from pydriller import Repository
import json

#reading a csv file using pandas:
def readcsv(pathurl)->pd.DataFrame:
    dataframe = pd.read_csv(pathurl)
    return dataframe

#deleting duplicated data:
def dropDuplicates(dataframe):
    dataframe.drop_duplicates(inplace=True)

#Extract meta data in a json file

def extract_commits_with_rgpd(repo_path,file_path):
    with open(file_path) as file:
        commits_with_rgpd=json.load(file)
    for commit in Repository(repo_path).traverse_commits():
        if 'RGPD' in commit.msg or 'GDPR' in commit.msg or 'gestion de vie privee' in commit.msg:
            commit_data = {
                'path':repo_path,
                'name':commit.project_name,
                'sha': commit.hash,
                'author': commit.author.name,
                'date': str(commit.author_date),
                'message': commit.msg,
                'insertions': commit.insertions,
                'lines' : commit.lines,
                'files' : commit.files,
                'dmm_unit_size' : commit.dmm_unit_size,
                'dmm_unit_complexity' : commit.dmm_unit_complexity
            }
            commits_with_rgpd.append(commit_data)
    with open(file_path, 'w') as file:
        json.dump(commits_with_rgpd, file, indent=4)


dt = readcsv('GDPR_commit.csv')
dropDuplicates(dt)
dt['URL']=dt['URL']+".git"

#extract_commits_with_rgpd("https://github.com/onOffice-Web-Org/oo-wp-plugin.git","file_path.json")

for index, row in dt.iterrows():
    path = str(row['URL'])
    extract_commits_with_rgpd(path,'output.json')
