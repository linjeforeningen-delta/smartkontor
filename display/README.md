### display.py

Launch display by navigating into the display folder and run `python3 display.py` in the command line.

The display is made using TkInter. It contains three modules: Bus departure times, cafeteria opening hours, and a clock.

### bussapi.py

Has the functions `busApi(busStop, num_calls)` and `getBuses(busStop, num_calls)`. 

`busApi(busStop, num_calls)` takes two arguments: a bus stop id in the form `'NSR:StopPlace:44085'` (from the National Stop place Registry, see https://developer.entur.org/content/nsr-0) and a number which decides how many bus departures to display. It returns a string in JSON format which contains the departure information of the next `num_calls` buses.

`getBuses(busStop, num_calls)` calls `busApi(busStop, num_calls)` and takes its return string and converts it into a python dictionary, then it retrieves the line number, destination, and departure time and returns them as three separate strings.

### cantinahours.py

Has the function `getCantinaHours()` which scrapes https://www.sit.no/mat for Realfagskantina's and Hangaren's opening hours and returns them as two seperate strings. This information is somewhat arbitrarily placed on the site, specifically in the 17th and 13th div tag of the class "eat-hours", so the function fetches the strings found in these specific tags. If SiT ever changes the layout of the site, this script will completely break.
