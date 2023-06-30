import os



class Config:
    AD_PATH_CSV = os.path.join("datasets", "csv_data", "ad.csv")
    AD_PATH_JSON = os.path.join("datasets", "json_data", "ad.json")

    CATEGORY_PATH_CSV = os.path.join("datasets", "csv_data", "category.csv")
    CATEGORY_PATH_JSON = os.path.join("datasets", "json_data", "category.json")

    LOCATION_PATH_CSV = os.path.join("datasets", "csv_data", "location.csv")
    LOCATION_PATH_JSON = os.path.join("datasets", "json_data", "location.json")

    USER_PATH_CSV = os.path.join("datasets", "csv_data", "user.csv")
    USER_PATH_JSON = os.path.join("datasets", "json_data", "user.json")
