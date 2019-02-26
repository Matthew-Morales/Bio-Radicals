# Bio-Radicals

## Directory Structure:
```
project
│   README.md
│   .gitignore
│   parse_customers.py
│   parse_lots.py
│   parse_reservations.py
│   parse_sales.py
│   reports_generator.py
│   sql queries
│   sql.txt
│   sqlite.py
│   ...
│
└─── Data folder
│   │   anemiasales.xlsx
│   │   Liquid IA Anemia data.xlsx
│   │   rReport.xlsx
│   │   ...
│   
└─── GeneratedReports folder
       │   customer1000005.xlsx
       │   customer1001883.xlsx
       │   customer1000239.xlsx
```

## git setup and common commands:

### Cloning (the working branch):
```
git clone -b working --single-branch https://github.com/Matthew-Morales/Bio-Radicals.git <optional: enter directory where you want to download the repository> 
```

### Check for status

```
git status
```

### Get up to date with the repository
```
git pull
```

### Committing:
```
git add -A
git commit -m "Enter the comment here"
git push
```


## .gitignore

In .gitignore, enter the file names you don't want git to push to the repository (excel sheets, IDE settings etc)

Currently, "pythonsqlite.db", "Data" folder, "GeneratedReports" folder, and all .xlsx files are ignored
