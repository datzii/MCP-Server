import os

server_port = os.getenv('server_port', 7600)
server_log_level = os.getenv('LOG_LEVEL', 'INFO')
server_host = os.getenv('server_host', 'localhost')


diagnosis_url = os.getenv('DIAGNOSIS_URL','http://localhost:5600/diagnosis_tool/get_prediction')
headers = {
    "Content-Type": "application/json"
}