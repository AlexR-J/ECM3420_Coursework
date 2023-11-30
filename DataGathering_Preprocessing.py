
import requests
import json
import time


def timer(n):  #creates a function called timer
    #create a count of the number of ░ and set it to 0 at the start.
    hash_count = 0
    print('')
    while n >= 0:
        #increament the ░ count every time the code runs
        hash_count += 1
        #create a variable containing the number spaces afer ░
        space_count = n - hash_count
        print('|'+'#'*hash_count+' '*n+'|', end="\r")
        #print ░ , and ' ' the rest up to n then every time it iterates
        #add one to the count of ░
        if n == 0:
            #if the time reaches 0 print times up and bretak the loop
            print('\nTIMES UP!')  #if times up stop and print times up
            break
        else:
            #else sleep for 1 seconf and then - one from n number of
            #seconds.
            time.sleep(1)  #else descrese the time and wait one second
            n -= 1

def getPlayersData():
    requestCount = 0
    file = open("newData.json", "w+")
    scanning = True
    count = 0
    page = 1
    api_key = "RGAPI-3207ab29-829f-4ec3-9922-e0982a4fdd29"
    queue = "RANKED_SOLO_5x5/"
    #division = input("Divsion? (In All Caps)") + "/"
    #tier = input("tier? (In Roman Numerals)") + "/"

    divisions = {
        "division":"BRONZE",
        "tier":"I"
        ,"rankId":1},{
        "division":"BRONZE",
        "tier":"II"
        ,"rankId":2}, {
        "division":"BRONZE",
        "tier":"III"
        ,"rankId":3},{
        "division":"BRONZE",
        "tier":"IV"
        ,"rankId":4}, {
        "division":"SILVER",
        "tier":"I"
        ,"rankId":5},{
        "division":"SILVER",
        "tier":"II"
        ,"rankId":6},{
        "division":"SILVER",
        "tier":"III"
        ,"rankId":7},{                
        "division":"SILVER",
        "tier":"IV"
        ,"rankId":8},{
        "division":"GOLD",
        "tier":"I"
        ,"rankId":9},{
        "division":"GOLD",
        "tier":"II"
        ,"rankId":10},{
        "division":"GOLD",
        "tier":"III"
        ,"rankId":11},{
        "division":"GOLD",
        "tier":"IV"
        ,"rankId":12},{
        "division":"PLATINUM",
        "tier":"I"
        ,"rankId":13},{
        "division":"PLATINUM",
        "tier":"II"
        ,"rankId":14},{
        "division":"PLATINUM",
        "tier":"III"
        ,"rankId":15},{
        "division":"PLATINUM",
        "tier":"IV"
        ,"rankId":16},{
        "division":"EMERALD",
        "tier":"I"
        ,"rankId":17},{
        "division":"EMERALD",
        "tier":"II"
        ,"rankId":18},{
        "division":"EMERALD",
        "tier":"III"
        ,"rankId":19},{
        "division":"EMERALD",
        "tier":"IV"
        ,"rankId":20},{
        "division":"DIAMOND",
        "tier":"I"
        ,"rankId":21},{
        "division":"DIAMOND",
        "tier":"II"
        ,"rankId":22},{
        "division":"DIAMOND",
        "tier":"III"
        ,"rankId":23},{
        "division":"DIAMOND",
        "tier":"IV"
        ,"rankId":24}

    newData = {"dataset":[]}
    for division in divisions:
        count = 0
        print("Currently Coimputing Division: " + division["division"] + " " + division["tier"])
        div = division["division"] + "/"
        tier = division["tier"] + "/"
        page = 1
        scanning = True
        while(scanning == True) :
            response = requests.get("https://euw1.api.riotgames.com/lol/league/v4/entries/" + queue + str(div) + str(tier) + "?page=" + str(page) + "&api_key=" + api_key)
            requestCount +=1
            print(response.status_code)

            file2 = open("testFile.txt", "w")
            data = json.dump(response.json(),file2, indent=4)
            file2.close()
            data2 = response.json()

            finished = False

            while(finished == False) :
                for item in data2 :
                    if(item["wins"] + item["losses"] >= 30) : 
                        if item["losses"] == 0 :
                            temp = {
                                "summonerId":item["summonerId"],
                                "wins":item["wins"],
                                "losses":item["losses"],
                                "winrate":100,
                                "rankId":division["rankId"]
                                }
                        else : 
                            temp = {
                                "summonerId":item["summonerId"],
                                "wins":item["wins"],
                                "losses":item["losses"],
                                "winrate":item["wins"]/item["losses"],
                                "rankId":division["rankId"]
                                }

                        newData["dataset"].append(temp)
                        #json.dump(temp, file, indent=4)
                        #file.write(",")
                        print("adding new player" + str(count))
                        count += 1
                        if count == 100:
                            finished = True
                            scanning = False
                            break
            page += 1
            print("newPage")

    for player in newData["dataset"] :
        response2 = requests.get("https://euw1.api.riotgames.com/lol/champion-mastery/v4/scores/by-summoner/" + player["summonerId"] + "?api_key=" + api_key)
        requestCount += 1
        print("RequestCount = " + str(requestCount))
        print(response2.status_code)
        newEntry = {"masteryScore":response2.json()}
        player.update(newEntry)
        response2 = requests.get("https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" + player["summonerId"] + "?api_key=" + api_key)
        requestCount += 1
        print("RequestCount = " + str(requestCount))
        data3 = response2.json()
        for champion in data3:
            newEntry = {"highestMastery":champion["championPoints"]}
            break;
        print(response2.status_code)
        player.update(newEntry)

        if requestCount >= 99 :
            timer(120)
            requestCount = 0


    json.dump(newData, file, indent=4)
if __name__ == "__main__":
    getPlayersData() 
    