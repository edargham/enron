# How to use:
## Requirements
To install the requirements run in your terminal:\
Bash:
```bash
$python3 -m pip install -r ./requirements.txt
```
Powershell / Command Prompt:
```powershell
python -m pip install -r ./requirements.txt
```

## Seeding the database:
Download the email dataset from [here](https://www.kaggle.com/datasets/wcukierski/enron-email-dataset) and unzip.

Enter the following information about your Neo4j database to be able to successfuly connect to Neo4j in the `config.json` file:
- `data_root_dir`: Path to your CSV data.
- `db_connection`: The connection url provided by your Neo4j Database.
- `db_name`: Database Name to stor the data in.

Then run in your terminal:\
Bash:
```bash
$python3 ./enron_csv_preprocess.py
```
Powershell / Command Prompt:
```powershell
python ./enron_csv_preprocess.py
```

To insert the data appropriately into the database.

## Running the queries:
A playground was provided in `main.py` for you to run the queries, after completing the previous sections just type your desired query function into `main.py` and run it in your terminal to print the results:\
Bash:
```bash
$python3 ./main.py
```
Powershell / Command Prompt:
```powershell
python ./main.py
```

 