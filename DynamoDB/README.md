# DynamoDB

If you are using a fresh [Cloud9 IDE](https://aws.amazon.com/cloud9/) to follow along with this lesson, you'll need to enable Python 3. In the Cloud9 preferences, go to **Python Support > Python Version** and select **Python 3**.

Install the `boto3` package as follows:

```sh
sudo pip-3.6 install boto3
```

## Walkthrough

### Create a Table

`python3 MoviesCreateTable.py`

### Load Sample Data

`python3 MoviesLoadData.py`

### Create, Read, Update, and Delete an Item

1. Create a New Item

    `python3 MoviesItemOps01.py`

2. Read an Item

    `python3 MoviesItemOps02.py`

3. Update an Item

    `python3 MoviesItemOps03.py`

4. Increment an Atomic Counter

    `python3 MoviesItemOps04.py`

5. Update an Item (Conditionally)

    `python3 MoviesItemOps05.py`

6. Delete an Item

    `python3 MoviesItemOps06.py`

### Query and Scan the Data

1. Query - All Movies Released in a Year

    `python3 MoviesQuery01.py`

1. Query - All Movies Released in a Year with Certain Titles

    `python3 MoviesQuery02.py`

1. Scan

    `python3 MoviesScan.py`

### Delete the Table

`python3 MoviesDeleteTable.py`