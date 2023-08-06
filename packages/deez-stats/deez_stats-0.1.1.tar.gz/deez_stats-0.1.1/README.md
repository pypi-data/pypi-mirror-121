![salt]
# deez_stats
Python connection to Yahoo! Fantasy API implementing the yahoo_fantasy_api from [spilchen] 

## Build Status

## Installation
Eventually, this package can be installed via pip:
```
pip install deez-stats
```
## Documentation

## Sample API Usage

#### history.db structure
All historical data is contained in history.db to offload API calls. This data also won't change and will only be updated
* manager  
  * Contains year, manager name, manager team name, manager id, league id, and game id  
* schedule  
  * Contains year, week, manager name, manager score, opponent name, opponent score, and result  
* playoff  
  * Contains year, playoff round, manager name, manager seed, manager score, opponent name, opponent seed, opponent score, and result  
* season_finish  
  * Contains year, manager name, and result only for playoffs  
* finances  
  * Contains year, manager name, buy in, and payout  


  [spilchen]: <https://github.com/spilchen/yahoo_fantasy_api>
  [salt]: <https://upload.wikimedia.org/wikipedia/en/thumb/b/b4/Morton_Salt_Umbrella_Girl.svg/320px-Morton_Salt_Umbrella_Girl.svg.png>