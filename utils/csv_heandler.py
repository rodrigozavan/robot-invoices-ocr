import csv


def read_csv(file_path):
    """
    Reads a CSV file and returns its contents as a list of dictionaries.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        list: A list of dictionaries, where each dictionary
        represents a row in the CSV file.
    """
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]

    return data


def write_csv(file_path, data):
    """
    Writes data to a CSV file.

    Args:
        file_path (str): The path to the CSV file.
        data (list): A list of dictionaries, where each dictionary
        represents a row in the CSV file.

    Returns:
        None
    """
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
