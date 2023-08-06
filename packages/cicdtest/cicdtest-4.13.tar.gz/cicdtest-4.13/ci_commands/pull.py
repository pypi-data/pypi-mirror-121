"""
    Title: pull.py
    Author: Kushagra A.
    Language: Python
    Date Created: 31-08-2021
    Date Modified: 23-09-2021
    Description:
        ###############################################################
        ## Check for pull operation on a repository   ## 
         ###############################################################
 """

from buildpan.previous_commit import prev_commit
import requests
from buildpan import setting, workflow, repo_pull, find_path
import click


info = setting.info


# getting env variable
push_commit = info["PUSH_COMMIT_URL"]


@click.command()
def pull():
    '''
     For manually trigger  pull operation

    \f
    '''

    all_repo_name = []
    try:
        find_path.find_path()
        file_path = find_path.find_path.file_path

        #reading data from centralized file
        with open(file_path + "/info.txt") as file:
            info = file.readlines()
            for data in info:
                d = eval(data)
                repo_name = d["repo_name"]
                repo_name_compare = repo_name.lower()
                repo_name = "repo_name="+repo_name.lower()
                all_repo_name.append(repo_name)
                
                # using pooling for pull operation
                response = requests.get(push_commit, repo_name)
                
                res=response.content
                res=str(res)
                index=res.index("'")
                index1=res.index("'",index+1)
                res=res[index+1:index1]
                res = res.lower()
        
                if repo_name_compare == res:
                    path = d["path"]
                    project_id = d["project_id"]
                    username = d["username"]
                    provider = d["provider"]

                    # doing pull operation
                    repo_pull.repo_pull(path, project_id, repo_name_compare, username, provider)
                            
                    # if pull success calling deployment        
                    response = workflow.workflows(path, project_id, repo_name_compare, username)
                   
                    # if deployment fails go to previous commit
                    if response == False:
                        prev_commit(path, repo_name, project_id, username, provider)
    
    except Exception as e:
        print("No CI-CD operation is running.")



