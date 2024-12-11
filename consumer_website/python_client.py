# Make sure to `pip install requests``
import requests


def download_brevets_csv():
    url = "http://localhost:5005/ListAll/csv"  # Resource URL
    try:
        # Make a GET request
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses

        # The CSV content will be in response.text
        csv_content = response.content.decode("utf-8")  # Decode the bytes to a string
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return

    # Just print the result for debugging, can also save to a file
    if csv_content:
        print(csv_content)
    else:
        print("No content found")


if __name__ == "__main__":
    download_brevets_csv()