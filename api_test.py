import requests




if __name__ == "__main__":
    # data = requests.post('http://127.0.0.1:5000/thread/single', data={'thread': 41})
    # rows = data.json()["rows"]
    # print rows

    # data = requests.post('http://127.0.0.1:5000/thread/quantity', data={'quantity': 5})
    # threads = data.json()["threads"]

    data = requests.post('http://127.0.0.1:5000/thread/all')
    all_threads = data.json()

    print all_threads["41"]