import pandas as pd
import argparse

DATA_ROOT = "~/Data/movies"
SCRIPTS_DEST = "./scripts/flyway"
CONFIGS = [{
        "source": f"{DATA_ROOT}/movies_metadata.csv",
        "destination": "movies_metadata",
        "out_file": f"{SCRIPTS_DEST}/V2__movie_metadata.sql",
        "primary_key_col": "id",
        "exclude_columns": ["belongs_to_collection", "genres", "poster_path","production_companies","production_countries", "spoken_languages", "tagline", "video"]
    },
    {
        "source": f"{DATA_ROOT}/ratings_small.csv",
        "destination": "movie_ratings",
        "out_file": f"{SCRIPTS_DEST}/V4__movie_ratings.sql",
        "dtypes": {"userId": int, "movieId": int}
    }
]

def clean_values(v, cast_type = None):
    """Generate a postgresql friendly string representation
    :param v: The value 
    :param cast_type: A python type to cast to (e.g. int, float)
    """
    if cast_type is not None:
        v = cast_type(v)
    if type(v) == str:
        v = str(v)
        v = v.replace("'","").replace("--",",").replace("\n", " ")
        v = f"'{v}'"
    return v

def dump_to_sql(source:str, destination:str, 
        exclude_columns:list = None, primary_key_col:str = None, out_file:str = None, dtypes:dict = {}):
    """Dump a dataframe to an insert values script
    """
    
    # Loading
    df = pd.read_csv(source)

    if exclude_columns is not None:
        df.drop(exclude_columns, axis=1, inplace=True)
    
    # Data Cleaning
    if primary_key_col is not None:
        df = df.drop_duplicates(subset=primary_key_col)

    # SQL Generation
    result_str = f"INSERT INTO {destination}({','.join(list(df.columns))}) VALUES \n"
    for _, row in df.iterrows():
        values = row.values.tolist()
        if len(values) == len(df.columns):
            row_data = '\t(' + (",".join([str(clean_values(v, dtypes.get(c))) for c,v in zip(df.columns, values)])) + '),\n'
            result_str += row_data
    result_str = result_str[:-2]

    # File Saving
    if out_file is None:
        print(result_str)
    else:
        with open(out_file, "x") as wf:
            wf.write(result_str)

if __name__ == "__main__":
    for c in [CONFIGS[1]]:
        dump_to_sql(**c)