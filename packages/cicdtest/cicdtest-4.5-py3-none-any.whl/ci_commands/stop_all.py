"""
    Title: stop_all
    Author: Kushagra A.
    Modified By: Kushagra A.
    Language: Python
    Date Created: 22-09-2021
    Date Modified: 21-09-2021
    Description:
        ###############################################################
        ##      Remove all repo details from centralized file        ## 
        ###############################################################
"""

import click
from click.decorators import command
import os
from buildpan import find_path
from crontab import CronTab

@click.command()
def stop_all():
    '''
     For stop CI-CD operation
    \f
    
   
    '''

    find_path.find_path()
    file_path = find_path.find_path.file_path

    if os.path.exists(file_path + "/info.txt"):
        os.remove(file_path + "/info.txt")
        print("CI-CD operation stopped \n Run:- buildpan init to intiate CICD operation")
    
    else:
        pass
    
    cron_job = CronTab(user=True)
    jobs= cron_job.find_comment('buildpan')
    jobs_list = list(jobs)
    if len(jobs_list) == 0:
        print("No buildpan process is runnig!!\n Run:- buildpan start to intiate buildpan operation")
    else:
        for job in jobs_list:
            cron_job.remove(job)
        cron_job.write()
        print("buildpan operation successfully stopped!")