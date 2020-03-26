import requests
import csv

response = requests.get("https://api-rezultati.sec.mk/Home/JsonResultsData?cs=en-US&r=1&rd=r&eu=all")

municipalities = response.json()["Menu"]["Municipalities"]
electoral_results = []

base_url = "https://api-rezultati.sec.mk/Home/JsonResultsData?cs=en-US&r=1&rd=r&eu=all&m="

for municipality in municipalities:
    municipality_result = requests.get("https://api-rezultati.sec.mk/Home/JsonResultsData?cs=en-US&r=1&rd=r&eu=all&m={munic}".format(munic = municipality["MunicipalityID"]))
    
    results_municipal = municipality_result.json()["Results"]["ResultsMain"]
    new_result = {}
    for result in results_municipal:
        new_result[result["CoalitionShortName"]] = result["CoalitionVotes"]
        new_result["municipality"] = municipality["MunicipalityName"]
        new_result["municipality_id"] = municipality["MunicipalityID"]
    electoral_results.append(new_result)

keys = electoral_results[0].keys()
with open('mkd_munic_results.csv', "w") as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(electoral_results)
