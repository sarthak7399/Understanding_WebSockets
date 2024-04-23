import json
import requests

headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNTM4ZGU5YjgtNmYxMi00N2U5LTk2OTktYjkzMmZkOGU5YmIwIiwidHlwZSI6ImFwaV90b2tlbiJ9.EoUxzL3GB2OWTTEqO3aYjJezH-L-OtG93K9OAHh9KIE"}


# import requests

# url = "https://api.edenai.run/v2/audio/text_to_speech"

# payload = {
#     "response_as_dict": True,
#     "attributes_as_list": False,
#     "show_original_response": False,
#     "rate": 0,
#     "pitch": 0,
#     "volume": 0,
#     "sampling_rate": 0
# }
# headers = {
#     "accept": "application/json",
#     "content-type": "application/json"
# }

# response = requests.post(url, json=payload, headers=headers)

# print(response.text)


url = "https://api.edenai.run/v2/audio/text_to_speech"
payload = {
    "providers": "google,amazon,openai", "language": "en",
    "option": "MALE",
    "text": "this is a test",
    "fallback_providers": ""
}

response = requests.post(url, json=payload, headers=headers)

result = json.loads(response.text)
print(result)
