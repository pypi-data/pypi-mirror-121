import logging
import requests
from urllib.parse import quote
from gitlab_client.config import GITLAB_BASE_URL_V4_DEFAULT
from gitlab_client.exceptions import (
    BranchError,
    JobError,
    MergeConflictError,
    MergeError,
    MergeRequestError,
    UnableToAcceptMR,
    PipelineError,
    TagError
)

logging.basicConfig(level=logging.INFO)


class Gitlab:
    """
    Return an instance of the given Gitlab project.

    Keyword arguments:
    project_id -- Id of the Gitlab project you want to instantiate and use. Can be found your repository's home page.
    access_token -- A personal access token generated from your Gitlab account.
                    See https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html on how to generate one.
    gitlab_base_url -- The base url where your repository is hosted.
    """
    def __init__(self, project_id, access_token, gitlab_base_url=GITLAB_BASE_URL_V4_DEFAULT, **kwargs):
        self.project_id = project_id
        self.access_token = access_token
        self.gitlab_base_url = gitlab_base_url
    
    # Branches
    def list_branches(self):
        """
        Returns list of branches.
        """
        response = self.__get(url="repository/branches")

        if response.ok:
            return response.json()
        
        error_message = response.json().get("message", response.reason)
        logging.error(f"Unable to get list of branches: {error_message}")
        raise BranchError(error_message)

    def get_branch(self, branch_name):
        """
        Returns the branch with the given name.

        Keyword arguments:
        branch_name -- Name of the branch you want to get.
        """
        encoded_branch_name = quote(branch_name, safe="")
        response = self.__get(url=f"repository/branches/{encoded_branch_name}")
        
        if response.ok:
            return response.json()
        else:
            error_message = response.json().get("message", response.reason)
            logging.error(f"Unable to get branch {branch_name}: {error_message}")
            raise BranchError(error_message)

    def create_branch(self, branch_name, branch_from):
        """
        Creates a branch with the given name.

        Keyword arguments:
        branch_name -- Name of the branch you want to create.
        branch_from -- Name of the branch you want to branch off from.
        """
        data={"branch": branch_name, "ref": branch_from}
        response = self.__post(url="repository/branches", data=data)
        
        if response.ok:
            logging.info(f"Created branch: {response.json()['name']}")
            #TODO: Return response ?
        else:
            error_message = response.json().get("message", response.reason)
            logging.error(f"Unable to create branch {branch_name}: {error_message}")
            raise BranchError(error_message)

    def get_or_create_branch(self, branch_name, branch_from):
        """
        Attempts to create and return a branch with given branch_name and branch_from.
        If a branch already exists, returns existing branch.

        Keyword arguments:
        branch_name -- Name of the branch you want to create.
        branch_from -- Name of the branch you want to branch off from.
        """
        try:
            branch = self.create_branch(branch_name, branch_from)
            return branch
        except BranchError as error:
            if error == "Branch already exists":
                branch = self.get_branch(branch_name)
                return branch
            else:
                error_message = f"Unable to get or create branch: {error}"
                logging.error(error_message)
                raise BranchError(error_message)
                

    def delete_branch(self, branch_name):
        """
        Deletes the branch with the given name.

        Keyword arguments:
        branch_name -- Name of the branch you want to delete.
        """
        response = self.__delete(url=f"repository/branches/{branch_name}")
        
        if response.ok:
            logging.info(f"Deleted branch: {branch_name}")
        else:
            error_message = response.json().get("message", response.reason)
            logging.error(f"Unable to delete branch {branch_name}: {error_message}")

    # Tags
    def get_tag(self, tag_name):
        """
        Returns the tag with the given name.

        Keyword arguments:
        tag_name -- Name of the tag you want to get.
        """
        response = self.__get(url=f"repository/tags/{tag_name}")

        json_response = response.json()
        if response.ok:
            return json_response
        else:
            error_message = json_response.get("message", response.reason)
            logging.error(f"Unable to get tag {tag_name}: {error_message}")
            raise TagError(error_message)

    def create_tag(self, tag_name, tag_on):
        """
        Creates a tag with the given tag_name on given ref.

        Keyword arguments:
        tag_name -- Name of the tag you want to create.
        tag_on -- Ref (Branch name or Commit SHA) you want to create the tag on.
        """
        data={"tag_name": tag_name, "ref": tag_on, "message": f"Automated release {tag_name}"}
        response = self.__post(url="repository/tags", data=data)
        
        json_response = response.json()
        if response.ok:
            logging.info(f"Created tag: {response.json()['name']}")
            return json_response
        else:
            error_message = response.json().get("message", response.reason)
            logging.error(f"Unable to create tag {tag_name}: {error_message}")
            raise TagError(error_message)

    def get_or_create_tag(self, tag_name, tag_on):
        """
        Attempts to create and return a tag with given tag_name and tag_on.
        If a tag already exists, returns existing tag.
        
        Keyword arguments:
        tag_name -- Name of the tag you want to create.
        tag_on -- Ref (Branch name or Commit SHA) you want to create the tag on.
        """
        try:
            tag = self.create_tag(tag_name, tag_on)
            return tag
        except TagError as error:
            print(error)
            if error == f"Tag {tag_name} already exists":
                tag = self.get_tag(tag_name)
                return tag
            else:
                error_message = f"Unable to get or create tag: {error}"
                logging.error(error_message)
                raise TagError(error_message)

    def delete_tag(self, tag_name):
        """
        Deletes tag with the given name.

        Keyword arguments:
        tag_name -- Name of the tag you want to delete.
        """
        response = self.__delete(url=f"repository/tags/{tag_name}")
        
        if response.ok:
            logging.info(f"Deleted tag: {tag_name}")
        else:
            error_message = response.json().get("message", response.reason)
            logging.error(f"Unable to delete tag {tag_name}: {error_message}")

    # Merge requests
    def get_merge_request(self, merge_request_iid):
        """
        Return merge request with the given iid. 

        Keyword arguments:
        merge_request_iid -- iid of the merge request you want to get.
        """
        response = self.__get(url=f"merge_requests/{merge_request_iid}")

        json_response = response.json()
        if response.ok:
            return json_response
        else:
            error_message = json_response.get("message", response.reason)
            logging.error(f"Unable to get merge request: {error_message}")
            raise MergeRequestError(error_message)
        
    def list_merge_requests(self, **kwargs):
        """
        Filter and return merge requests based on given filter params.

        keyword arguments:
        **kwargs -- Dictionary of filter params.
        """
        response = self.__get(url="merge_requests", params=kwargs)

        json_response = response.json()
        if response.ok:
            return json_response
        else:
            error_message = json_response.get("message", response.reason)
            logging.error(f"Unable to filter merge requests: {error_message}")
            raise MergeRequestError(error_message)

    def create_merge_request(self, source_branch, target_branch, title, **kwargs):
        """
        Create a merge request.

        Keyword arguments:
        source_branch -- Source branch name for the merge request.
        target_branch -- Target branch name for the merge request.
        title -- Title of the merge request.
        **kwargs -- Any additional options you want to pass.
        """
        data={"source_branch": source_branch, "target_branch": target_branch, "title": title, **kwargs}
        response = self.__post(url="merge_requests", data=data)
        
        json_response = response.json()
        if response.ok:
            logging.info(f"Created merge request: {json_response['iid']} - {json_response['title']}")
            return json_response
        else:
            error_message = json_response.get("message", response.reason)
            logging.error(f"Unable to create merge request: {error_message}")
            raise MergeRequestError(error_message)
    
    def get_or_create_merge_request(self, source_branch, target_branch, title, **kwargs):
        """
        Attempts to create and return a merge request with given source_branch, target_branch, title, and kwargs.
        If a merge request already exists, returns existing merge request.

        Keyword arguments:
        source_branch -- Source branch name for the merge request.
        target_branch -- Target branch name for the merge request.
        title -- Title of the merge request.
        **kwargs -- Any additional options you want to pass.
        """
        try:
            new_merge_request = self.create_merge_request(source_branch, target_branch, title, **kwargs)
            logging.info(f"Created merge request: {new_merge_request['iid']} - {new_merge_request['title']}")
            return new_merge_request
        except MergeRequestError as e:
            for message in e:
                if message.startswith("Another open merge request already exists for this source branch"):
                    merge_request_iid = message.split("!")[1]
                    merge_request = self.get_merge_request(merge_request_iid)
                    logging.info(
                        f"Unable to create new merge request because one already exists "
                        f"for this source branch: {merge_request['iid']} - {merge_request['title']}"
                    )
                    return merge_request
            
            error_message = f"Unable to get or create merge request: {e}"
            logging.error(error_message)
            raise MergeRequestError(error_message)

    def update_merge_request(self, merge_request_iid, **kwargs):
        """
        Updates the given merge request with new given parameters.

        Keyword arguments:
        merge_reques_iid -  iid of the merge request you want to update.
        """
        data = {**kwargs}
        response = self.__put(url=f"merge_requests/{merge_request_iid}", data=data)

        json_response = response.json()
        if response.ok:
            logging.info(f"Updated merge request: {json_response['iid']}")
            return json_response
        else:
            error_message = json_response.get("message", response.reason)
            logging.error(f"Unable to update merge request: {error_message}")
            raise MergeRequestError(error_message)

    def delete_merge_request(self, merge_request_iid):
        """
        Delete merge request with the given iid.

        Keyword arguments:
        merge_request_iid - iid of the merge request you want to delete.
        """
        response = self.__delete(url=f"merge_request/{merge_request_iid}")
        
        if response.ok:
            logging.info(f"Deleted merge request: {merge_request_iid}")
        else:
            error_message = response.json().get("message", response.reason)
            logging.error(f"Unable to delete merge request {merge_request_iid}: {error_message}")

    def accept_mr(self, merge_request_iid):
        """
        Attempt to merge given merge request. Raises error if unable to merge.

        Keyword arguments:
        merge_request_iid - iid of the merge request you want to merge.
        """
        response = self.__put(url=f"merge_requests/{merge_request_iid}/merge")
        
        json_response = response.json()
        if response.ok:
            logging.info(f"Accepted merge request: {json_response['iid']} - {json_response['title']}")
        else:
            error_message = json_response.get("message", response.reason)
            logging.error(f"Unable to accept merge request {merge_request_iid}: {error_message}")
            if response.status_code == 401:
                logging.error(f"Unable to accept merge request because you don't have permissions to accept this merge request.")
                raise PermissionError(error_message)
            elif response.status_code == 405:
                logging.error(f"Unable to accept merge request because it is either a Draft, Closed, Pipeline Pending Completion, or Failed while requiring Success.")
                raise UnableToAcceptMR(error_message)
            elif response.status_code == 406:
                logging.error(f"Unable to accept merge request because of conflicts.")
                raise MergeConflictError(error_message)
            raise MergeError(error_message)

    # Pipelines
    def list_pipelines(self, **kwargs):
        """
        Filter and return pipelines based on given filter params.

        keyword arguments:
        **kwargs -- Dictionary of filter params.
        """
        response = self.__get(url="pipelines", params=kwargs)

        json_response = response.json()
        if response.ok:
            return json_response
        else:
            error_message = json_response.get("message", response.reason)
            logging.error(f"Unable to filter pipelines: {error_message}")
            raise PipelineError(error_message)

    def get_pipeline(self, pipeline_id):
        """
        Return the pipeline with given pipeline_id

        Keyword arguments:
        pipeline_id - id of the pipeline you want to get.
        """
        response = self.__get(url=f"pipelines/{pipeline_id}")
        
        json_response = response.json()
        if response.ok:
            return json_response
        else:
            error_message = json_response.get("message", response.reason)
            logging.error(f"Unable to get pipeline: {error_message}")
            raise PipelineError(error_message)
    
    def list_merge_request_pipelines(self, merge_request_iid):
        """
        List all pipelines for given merge_request_iid

        Keyword arguments:
        merge_request_iid - iid of the merge request for which you want to list pipelines.
        """
        response = self.__get(url=f"merge_requests/{merge_request_iid}/pipelines")

        json_response = response.json()
        if response.ok:
            return json_response
        else:
            error_message = json_response.get("message", response.reason)
            logging.error(f"Unable to get pipelines for merge request {merge_request_iid}: {error_message}")
    
    def list_pipeline_jobs(self, pipeline_id, scopes=[]):
        """
        List all jobs for given pipeline filtered by given scopes.

        Keyword arguments:
        pipeline_id - id of the pipeline for which you want to list jobs.
        """
        params = {
            "scope[]": scopes
        }
        response = self.__get(url=f"pipelines/{pipeline_id}/jobs", params=params)
        
        json_response = response.json()
        if response.ok:
            return json_response
        else:
            error_message = json_response.get("message", response.reason)
            logging.error(f"Unable to get jobs for pipeline {pipeline_id}: {error_message}")

    def get_next_pipeline_job(self, pipeline_id):
        """
        Return next manual job for given pipeline.

        Keyword arguments:
        pipeline_id - id of the pipeline.
        """
        manual_pipeline_jobs = self.list_pipeline_jobs(pipeline_id, scopes=["manual"])
        
        return manual_pipeline_jobs[-1] if manual_pipeline_jobs else []
        
    def play_job(self,  job_id):
        """
        Run the given job.

        Keyword arguments:
        job_id - id of the job you want to run.
        """
        response = self.__post(url=f"jobs/{job_id}/play")

        json_response = response.json()
        if response.ok:
            logging.info(f"Running job: {json_response['id']} - {json_response['name']}")
        else:
            error_message = json_response.get("message", response.reason)
            logging.error(f"Unable to play job {job_id}: {error_message}")
            raise JobError(error_message)
        
    def __get(self, url, params={}):
        response = requests.get(
            f"{self.gitlab_base_url}/projects/{self.project_id}/{url}",
            headers={"PRIVATE-TOKEN": self.access_token},
            params=params
        )

        return response
    
    def __put(self, url, data={}):
        response = requests.put(
            f"{self.gitlab_base_url}/projects/{self.project_id}/{url}",
            headers={"PRIVATE-TOKEN": self.access_token},
            data=data
        )

        return response
    
    def __post(self, url, data={}):
        response = requests.post(
            f"{self.gitlab_base_url}/projects/{self.project_id}/{url}",
            headers={"PRIVATE-TOKEN": self.access_token},
            data=data
        )

        return response
    
    def __delete(self, url):
        response = requests.delete(
            f"{self.gitlab_base_url}/projects/{self.project_id}/{url}",
            headers={"PRIVATE-TOKEN": self.access_token}
        )

        return response
