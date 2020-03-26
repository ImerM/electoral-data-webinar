import requests
import csv

response = requests.get("https://api-rezultati.sec.mk/Home/JsonResultsData?cs=en-US&r=1&rd=r&eu=all")

municipalities = response.json()["Menu"]["Municipalities"]

base_url = "https://api-rezultati.sec.mk/Home/JsonResultsData?cs=en-US&r=1&rd=r&eu=all&m="


with open('mkd_polling_results.csv', "w") as output_file:
    for municipality in municipalities:
        municipality_result = requests.get("https://api-rezultati.sec.mk/Home/JsonResultsData?cs=en-US&r=1&rd=r&eu=all&m={munic}".format(munic = municipality["MunicipalityID"]))
        
        results_municipal = municipality_result.json()["Results"]["ResultsMain"]
        for result in results_municipal:
            electoral_results = []
            for station in municipality_result.json()["Menu"]["PollinStations"]:
                results_mb = requests.get("https://api-rezultati.sec.mk/Home/JsonResultsData?cs=en-US&r=1&rd=r&eu=all&m={munic}&ps={ps}".format(munic = municipality["MunicipalityID"], ps = station["PollingStationID"]))
                ps_result = {}
                print(station["PollingStationID"])
                for p_entry in results_mb.json()["Results"]["ResultsMain"]:        
                    ps_result[p_entry["CoalitionShortName"]] = p_entry["CoalitionVotes"]
                    ps_result["municipality"] = municipality["MunicipalityName"]
                    ps_result["municipality_id"] = municipality["MunicipalityID"]
                    ps_result["station_name"] = station["PollingStationName"]
                    ps_result["station_id"] = station["PollingStationID"]
                electoral_results.append(ps_result)
                if len(electoral_results) == 1:
                    keys = electoral_results[0].keys()
                    dict_writer = csv.DictWriter(output_file, keys)
                    dict_writer.writeheader()
            dict_writer.writerows(electoral_results)



        
        
