import requests
import json
import common.config as config

def classify_brain_tumor_from_MRI_function(image_path: str) -> str:
    ''' Classifies brain tumor of the specific image '''
    
    post_data = {
        "file_path": image_path
    }
    try:
        response = requests.post(url = config.diagnosis_url, headers = config.headers, data = json.dumps(post_data))
        if response.status_code != 200:
            raise Exception(f"Error al obtener respuesta {response.text}")
        
        response_data = response.json()
        print(f'-- Response {response_data}')
        final_answer = response_data.get('response')

        return final_answer

    except Exception as err:
        print("Error extracting response ", err)