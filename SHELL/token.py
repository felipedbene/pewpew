#!python3
import requests

url = "https://10.4.29.121/api/"

querystring = {"type":"keygen","user":"gogvale","password":"57%25fkObmcnYlI3XOcP7f"}

headers = {
    'Cache-Control': "no-cache",
    'Postman-Token': "63c1fdd6-6792-4498-b423-72ee6a5e152e"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
