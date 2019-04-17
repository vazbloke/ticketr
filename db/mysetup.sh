# mongoimport --db northpark --collection user <jsondata/User.json

# mongoimport -d northpark -c user --jsonArray -file <jsondata/User.json
# mongoimport -d northpark -c data --jsonArray -f <jsondata/"Sample Data.json"

# mongoimport --db northpark --collection data <jsondata/"Sample Data.json"

mongoimport --db northpark --collection user --file jsondata/User.json --jsonArray

mongoimport --db northpark --collection data --file jsondata/"Sample Data.json" --jsonArray