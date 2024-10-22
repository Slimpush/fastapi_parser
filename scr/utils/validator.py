def is_valid_year(date_str: str) -> bool:
    year = int(date_str.split(".")[2])
    return year == 2023 or year == 2024
