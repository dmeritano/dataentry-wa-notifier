class Config():

    JOBS_DATA_FOLDER = "./data"

    #Json parameters - Used internally in this class
    PARAM_WAPP_AUTH_TOKEN = "wappAuthToken"
    PARAM_WAPP_API_URL = "wappApiUrl"
    PARAM_SEND_MESSAGE_WITH_SAME_DATA = "sendMessageWithSameData"
    PARAM_JOBS_LIST = "jobs"
    PARAM_JOB_FACTORY_PROCESS = "factoryProcess"
    PARAM_JOB_DESCRIPTION = "description"
    PARAM_JOB_WAPP_TEMPLATE = "wappTemplate"
    PARAM_JOB_DMS_URI = "dmsUri"
    PARAM_JOB_DMS_USER = "dmsUser"
    PARAM_JOB_DMS_PASS = "dmsPass"
    PARAM_JOB_DMS_QUERIES = "dmsQueries"
    PARAM_JOB_DMS_QUERIES_QUERY_STRING = "query"
    PARAM_JOB_DMS_QUERIES_QUERY_DESCRIPTION = "queryDescription"
    PARAM_JOB_WAPP_RECIPIENTS = "wappRecipients"
    
    
    app_cfg = None
    
    def __init__(self, cfg):
        self.app_cfg = cfg
    
    def get_jobs_data_folder(self):
        return self.JOBS_DATA_FOLDER
    
    #Json values - Return
    def get_wapp_auth_token(self):
        return self.app_cfg[self.PARAM_WAPP_AUTH_TOKEN]

    def get_wapp_api_url(self):
        return self.app_cfg[self.PARAM_WAPP_API_URL]

    def get_jobs(self):
        return self.app_cfg[self.PARAM_JOBS_LIST]

    def get_jobs_number(self):
        return len(self.app_cfg[self.PARAM_JOBS_LIST])

    def get_job_factory_process(self, job):
        return job[self.PARAM_JOB_FACTORY_PROCESS]

    def get_job_description(self, job):
        return job[self.PARAM_JOB_DESCRIPTION]

    def get_job_wapp_template(self, job):
        return job[self.PARAM_JOB_WAPP_TEMPLATE]

    def get_job_dms_uri(self, job):
        return job[self.PARAM_JOB_DMS_URI]

    def get_job_dmsuser_name(self, job):
        return job[self.PARAM_JOB_DMS_USER]

    def get_job_dmsuser_pass(self, job):
        return job[self.PARAM_JOB_DMS_PASS]

    def get_job_queries(self, job):
        return job[self.PARAM_JOB_DMS_QUERIES]

    def get_query_string(self, query):
        return query[self.PARAM_JOB_DMS_QUERIES_QUERY_STRING]

    def get_query_description(self, query):
        return query[self.PARAM_JOB_DMS_QUERIES_QUERY_DESCRIPTION]

    def get_send_msg_with_same_data(self, job):
        return job[self.PARAM_SEND_MESSAGE_WITH_SAME_DATA]

    def get_job_wapp_recients(self, job):
        return job[self.PARAM_JOB_WAPP_RECIPIENTS]


        