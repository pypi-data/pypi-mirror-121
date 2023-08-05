"""
    Title: previous_commit
    Author: Kushagra A.
    Language: Python
    Date Created: 14-09-2021
    Date Modified: 14-09-2021
    Description:
        ###############################################################
        ## Get previous commit of a repository   ## 
         ###############################################################
 """

import subprocess
from buildpan import setting
import requests, datetime

info = setting.info

# getting env variable
get_sha = info["GET_SHA_URL"]
fetch_log = info["FETCH_LOG_URL"]


def prev_commit(path, repo_name, project_id, username):
    try:
        curtime = datetime.datetime.now()

        # pooling to get sha for the previous commit
        response = requests.get(get_sha, repo_name)
        res=response.content
        res=str(res)
        index=res.index("'")
        index1=res.index("'",index+1)
        res=res[index+1:index1]

        # restoring to previous commit
        subprocess.call(["git", "fetch", "origin", res], cwd=path)
        result = subprocess.call(["git", "checkout", "FETCH_HEAD"], stdout= subprocess.PIPE, stderr = subprocess.STDOUT, cwd=path)

        requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=Pull = '+str(result.stdout.decode())+'&status=success&operation=previous commit')

    except Exception as e:
        requests.post(fetch_log + "?" +'project_id='+project_id+'&repo_name='+repo_name+'&Time='+str(curtime)+'&user_name='+username+'&message=Pull = '+str(e)+'&status=failed&operation=previous commit')
