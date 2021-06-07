# educhain

educhain is a POC flask app whose purpose is to leverage blockchain POW & network consensus to securely send data payloads of an arbitrary type. 

## To run

Clone the repository & install dependncies

```bash
cd ../PATHTOREPO/
pip install -r requirements.txt
```

now run the app locally

```bash
python3 app.py
```

## Usage
The app supports 3 endpoints currently. One for queuing artificial data transactions, one for mining queued transactions & adding to chain, and one for viewing metadata about the chain. 

Add a block to the chain: this one contains a students semester marks. 
```bash
curl --location --request POST 'http://127.0.0.1:5000//transactions/new' \
--header 'Content-Type: text/plain' \
--data-raw '{
    "sender": "0038nsSJDsdDUMMYSENDERXNxmsonasdX28",
    "recipient": "0038nsSJDsdDUMMYRECEPIENTXNxmsonasdX28",
    "payload": {
        "MATH-102": 95,
        "BIO-101": 82,
        "BIO-101L": 86,
        "ART-311": 91
    },
    "amount": 5
}'
```

Now mine the block you just added:

```bash
curl --location --request GET 'http://127.0.0.1:5000/mine'
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
