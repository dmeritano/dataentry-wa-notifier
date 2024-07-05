# WhatsApp Functions
import requests

# Allowed templates
TEMPLATES_ONE = "notification_two_queries"


def send_notification(api_url, api_token, template, to, components_body_parameters):
    
    if template.lower() == TEMPLATES_ONE:
        status, response = send_message_template_one(api_url,
                                                     api_token,
                                                     template,
                                                     to,
                                                     components_body_parameters)

        if (status and response):
            message_status = response["messages"][0]["message_status"]
            message_id = response["messages"][0]["id"]
            if (message_status == "accepted"):
                return True, message_id
            else:
                return False, "Message was not accepted by WhatsApp API"
        else:
            False, response

    else:
        return False, f"Template {template} not implemented"


def send_message_template_one(api_url, api_token, template, to, components_body_parameters):

    headers = {
        'Authorization': 'Bearer ' + api_token,
        'Content-Type': 'application/json',
    }

    json_data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "template",
        "template": {
            "name": template,
            "language": {
                "code": "es_AR"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {
                            "type": "text",
                            "text": components_body_parameters[0]
                        },
                        {
                            "type": "text",
                            "text": components_body_parameters[1]
                        },
                        {
                            "type": "text",
                            "text": components_body_parameters[2]
                        }
                    ]
                }
            ]
        }}

    try:
        response = requests.post(api_url, headers=headers, json=json_data)
        if response.status_code != 200:
            return False, None
        else:
            return True, response.json()
    except Exception as error:
        msg = f'Error sending message {error.args}'
        return False, msg
