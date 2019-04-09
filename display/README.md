### display.py

WIP

### bussapi.py

WIP

### cantinahours.py

Has the function `getCantinaHours()` which scrapes https://www.sit.no/mat for Realfagskantina's and Hangaren's opening hours and returns them as two seperate strings. This information is somewhat arbitrarily placed on the site, specifically in the 17th and 13th div tag of the class "eat-hours", so the function fetches the strings found in these specific tags. If SiT ever changes the layout of the site, this script will completely break.
