import json
def save_to_json_file(json_data, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)