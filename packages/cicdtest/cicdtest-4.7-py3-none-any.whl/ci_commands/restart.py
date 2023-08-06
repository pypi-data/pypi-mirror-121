"""
    Title: stop_all
    Author: Kushagra A.
    Modified By: Kushagra A.
    Language: Python
    Date Created: 27-09-2021
    Date Modified: 27-09-2021
    Description:
        ###############################################################
        ##      Remove all repo details from centralized file        ## 
        ###############################################################
"""


import click
from click.decorators import command
from buildpan import stop_job
from ci_commands import start

@click.command()
def restart():
    '''
     For restart CI-CD operation
    \f
    
   
    '''
    response = stop_job.stop_job()

    if response == True:
        start.start()

