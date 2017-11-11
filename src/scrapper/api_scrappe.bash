while :
do
    TIME="`date +%Y%m%d_%H%M%S`";

    ROUTE='10'
    curl 'https://realtimetcatbus.availtec.com/InfoPoint/rest/Vehicles/GetAllVehiclesForRoutes?routeIDs='$ROUTE -H 'Pragma: no-cache' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.8,la;q=0.6' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: https://realtimetcatbus.availtec.com/InfoPoint/' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Cache-Control: no-cache' --compressed > "api_results/route$ROUTE/$TIME.json"

    ROUTE='11'
    curl 'https://realtimetcatbus.availtec.com/InfoPoint/rest/Vehicles/GetAllVehiclesForRoutes?routeIDs='$ROUTE -H 'Pragma: no-cache' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.8,la;q=0.6' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: https://realtimetcatbus.availtec.com/InfoPoint/' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Cache-Control: no-cache' --compressed > "api_results/route$ROUTE/$TIME.json"

    ROUTE='15'
    curl 'https://realtimetcatbus.availtec.com/InfoPoint/rest/Vehicles/GetAllVehiclesForRoutes?routeIDs='$ROUTE -H 'Pragma: no-cache' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.8,la;q=0.6' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: https://realtimetcatbus.availtec.com/InfoPoint/' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Cache-Control: no-cache' --compressed > "api_results/route$ROUTE/$TIME.json"

    ROUTE='17'
    curl 'https://realtimetcatbus.availtec.com/InfoPoint/rest/Vehicles/GetAllVehiclesForRoutes?routeIDs='$ROUTE -H 'Pragma: no-cache' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.8,la;q=0.6' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: https://realtimetcatbus.availtec.com/InfoPoint/' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Cache-Control: no-cache' --compressed > "api_results/route$ROUTE/$TIME.json"

    ROUTE='81'
    curl 'https://realtimetcatbus.availtec.com/InfoPoint/rest/Vehicles/GetAllVehiclesForRoutes?routeIDs='$ROUTE -H 'Pragma: no-cache' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.8,la;q=0.6' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: https://realtimetcatbus.availtec.com/InfoPoint/' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Cache-Control: no-cache' --compressed > "api_results/route$ROUTE/$TIME.json"

    ROUTE='82'
    curl 'https://realtimetcatbus.availtec.com/InfoPoint/rest/Vehicles/GetAllVehiclesForRoutes?routeIDs='$ROUTE -H 'Pragma: no-cache' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-US,en;q=0.8,la;q=0.6' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Referer: https://realtimetcatbus.availtec.com/InfoPoint/' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Cache-Control: no-cache' --compressed > "api_results/route$ROUTE/$TIME.json"

    sleep 5

done
