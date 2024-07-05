import logging
import os
import os.path
import json
from datetime import datetime
from time import sleep
from random import randint

#import Config
from config import Config
from whatsapp import api_wapp
from dms import api_dms

# App Config
cfg = None

app_config = Config({})

# Logging system
logger = logging.getLogger(__name__)

def start(config):
    global app_config
    app_config = config
        
    msg = f"Main process started. Jobs run:{app_config.get_jobs_number()}"
    logger.info(msg)
        
    for idx, job in enumerate(app_config.get_jobs()):
        template = app_config.get_job_wapp_template(job)
        if template == "notification_two_queries":
            run_job_one(job, idx)
        else:
            msg = f"Process for job index {idx}, template '{template}' is not implemented"
            logger.error(msg)
    

def run_job_one(job, job_index):
    msg = None
    st_login = None
    documents_first_query = 0
    documents_second_query = 0
    job_name = app_config.get_job_description(job)
    try:        
        msg = f"Runing job '{job_name}' - Index: {job_index}"
        logger.info(msg)

        #Api Dms parameters
        dms = app_config.get_job_dms_uri(job)
        user = app_config.get_job_dmsuser_name(job)
        password = app_config.get_job_dmsuser_pass(job)
        
        #Get the result of the 2 queries configured for this job/template
        #Template: notification_two_queries must have two queries - Exactly two queries
        #Setp 1 - Auth
        st_login = api_dms.login(dms,user,password,False)
        if not st_login:
            return None
        
        #Step 2 - Get Documents count for first query
        jobs_queries = app_config.get_job_queries(job)
        query = app_config.get_query_string(jobs_queries[0])  #job[config.PARAM_JOBS_DMS_QUERIES][0][config.PARAM_JOBS_DMS_QUERIES_QUERY]
        response = api_dms.get_documents_by_query(query,"$#TModificado",None,None,True)
        if response:
            documents_first_query = int(response["meta"]["total"])

        #Step 2 - Get Documents count for second query
        query = app_config.get_query_string(jobs_queries[1])  #job[config.PARAM_JOBS_DMS_QUERIES][0][config.PARAM_JOBS_DMS_QUERIES_QUERY]
        response = api_dms.get_documents_by_query(query,"$#TModificado",None,None,True)
        if response:
            documents_second_query = int(response["meta"]["total"])

        current_job_data = {
            "name":job_name,
            "documents_first_query": documents_first_query,
            "documents_second_query": documents_second_query,
            "last_run": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        #Step 3 - Check if results differs from las run
        send_message = True
        if not app_config.get_send_msg_with_same_data(job):

            last_data = get_job_last_run_data(job_index)
            if last_data:
                if ( last_data["documents_first_query"] == documents_first_query and 
                    last_data["documents_second_query"] == documents_second_query):
                    msg = f'There is no job changes from last run'
                    logger.info(msg)
                    send_message = False

        #Job Data File must be update always
        save_job_data(job_index, current_job_data)

        #Step 4
        #Si hay que enviar mensaje, aqui habría que enviarlos
        if send_message:            
            recipients = app_config.get_job_wapp_recients(job) 
            for to in recipients:
                logger.info(f"Sending message to {to}")

                
                #template_variable_one = app_config.get_query_description(jobs_queries[0])

                template_variable_one = app_config.get_job_factory_process(job)
                template_variable_two = app_config.get_query_description(jobs_queries[0])
                template_variable_two += ": [ " + " ".join(str(documents_first_query)) + " ]"
                template_variable_three = app_config.get_query_description(jobs_queries[1])
                template_variable_three += ": [ " + " ".join(str(documents_second_query)) + " ]"

                st, message = api_wapp.send_notification(app_config.get_wapp_api_url(),
                        app_config.get_wapp_auth_token(),
                        app_config.get_job_wapp_template(job),
                        to,
                        [template_variable_one, template_variable_two, template_variable_three])

                if (st):
                    msg = f"Message delivered to {to} - Message ID:{message}"
                    logger.info(msg)
                else:
                    msg = f"Message to {to} was not delivered. Reason: {message}"                    
                    logger.error(msg)
            
                sleep(randint(2,10))

        else:
            msg = f"Do not have to send a message for this job {job_name}"
            logger.info(msg)

    except Exception as error:
        msg = f"Error running job: {error.args}"
        logger.error(msg)        
    finally:
        if st_login:
            api_dms.logout()

    return None
    

def get_job_last_run_data(job_index):
    try:
        job_file = f"{app_config.get_jobs_data_folder()}/job_{job_index}.json"
        if os.path.isfile(job_file):
            with open(job_file, "r", encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)
                return data
        else:
            msg = f'File {job_file} does not exist'
            logger.info(msg)
    except Exception as error:
        msg = f"Error getting last run data for job {job_index}: {error.args}"
        logger.error(msg)        
    
    return None

def save_job_data(job_index, job_data):
    try:        
        job_file = f"{app_config.get_jobs_data_folder()}/job_{job_index}.json"        
        with open(job_file, "w", encoding='utf-8') as file:
            json.dump(job_data, file, ensure_ascii=False)
            return True
    except Exception as error:
        msg = f"Error saving last run data for job {job_index}, file: {job_file} : {error.args}"
        logger.error(msg)            
    
    return False