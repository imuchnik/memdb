# Simple in memory database in python
 ## Available Functions:
- SET [name] [value] : -- Sets the name in the database to the given value
- GET [name] :
Prints the value for the given name. If the value is not in the database, prints N​ ULL
- DELETE [name] : 
Deletes the value from the database
- COUNT [value] :
Returns the number of names that have the given value assigned to them. If that value is not assigned anywhere, prints ​0
- END:  Exits the database

###The database must also support transactions:
- BEGIN: Begins a new transaction
- ROLLBACK :
Rolls back the most recent transaction. If there is no transaction to rollback, prints "T​RANSACTION NOT FOUND"
- COMMIT : Commits a​ ll​ of the open transactions

## Requirements
- virtualenv
- python 3.6
- pytest 
- other packages outlined in requirements.txt
## Getting started
```
source venv/bin/activate
pip install -r requirements.txt
python memdb.py
```

## Testing
To execute tests simply run:
```$xslt
pytest -v

```
