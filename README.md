# Local Politics Data Crunching
A github repo for keep tracking of mini data projects around voter outreach and local politics
#

# Requirements
This project uses poetry as a package manager for python.
If you have a poetry setup you should be able to use poetry to run the scripts in this repo by activating the poetry environment.
If not the specific requirements are located in pyproject.toml.

# Data
The voter data from the board of elections is around 900k lines and contains identifable information about voters.

In light of the size of the data and the fact I didn't feel comfortable directly uploading idenfiable info to github, I have included artifical data in the folder `test_data` to use for testing/demo purposes.

The real data that I am basing this off that this code is designed to work with can be found at the data/maps section of the cuyahoga county board of elections website here: https://boe.cuyahogacounty.gov/maps-and-data

Specically at this link: https://cuyahogaelectionaudits.us/downloads/rvht/rvht.csv

The file `test_data/boe_data.csv` is the artifical board of elections data

The file `test_data/voter_data.csv` is artifical data representing a manual spreadsheet of voter information of the type you might have a local political club or campaign. Some data such as the voters address might be missing. Their name might not also match the official boe data.

For scripts that use `test_data/boe_data.csv`, simply running the same script on the data from board of elections (see above)
will yield real results instead of artificial ones.

# Projects/Scripts

## board of elections voter data
The board of elections spreadsheet has almost 900k lines. Manually looking up voters in their is time intensive.
The following mini projects were meant to get information from this spreadsheet quickly using pythons pandas package.

A lot of these scripts are designed to work for my specific use case, however they all generally have python functions that solve the more general problem.
For instance, one of the scripts looks up voters in my voting precinct; however it leverages a function that can be used for any precinct.

### find_precincts_from_boe.py
This script takes in a spreadsheet of names and/or addresses, looks them up in the board of elections spreadsheet and then adds their name, address, precinct, and ward to a new spreadsheet.

How to run:
 ```shell
python -m local_politics.find_precincts_from_boe test_data/voter_data.csv test_data/boe_data.csv --by_name --by_address
```
Using the "--by_name" flag will create an output file matching voters using their first and last names

Using the "--by_address" flag will create an output file matching voters using their address

Using both will create both files

### new_voters.py
This script finds new voters in Cleveland Heights. Specifically creates output spreadsheets based on if any of three recent elections were their first time voting.

How to run:
```
python -m local_politics.new_voters test_data/boe_data.csv
```

### search_precinct.py
This script finds new voters in my ward/precinct in Cleveland Heights (CH3D).

How to run:
```
python -m local_politics.search_precinct test_data/boe_data.csv
```

### young_voters.py
This script finds voters under 25 or 35 in Cleveland Heights

How to run:
```
python -m local_politics.young_voters test_data/boe_data.csv
```
