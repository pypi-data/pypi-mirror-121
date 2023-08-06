<h1 align="center">eztransfer</h1>

<center>Simple tool that makes moving your files between different storage providers easier.</center>

---

**eztransfer** is taking care of this time-consuming and boring operations.

- You have access to various handles (see `Supported Services`) or even implement your own! (by using interface)
- You don't need to think about transferred files being on your hard drive. Just specify where your files are and where you want them to be.

If you just need to transfer files from A to B, or B to A, this is the right tool! It's aimed for simple operations. 

<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

- Python 3.6+

### Installation

Ultimately, there will be a pip package.

Just for now:
1. Clone repository
```
git clone https://github.com/mbroton/ez-transfer.git
```
2. Create python virtual environment, activate it
```
virtualenv venv
source venv/bin/activate
```
3. Install requirements
```
pip install -r requirements.txt
```

<!-- USAGE EXAMPLES -->

## Usage

```python
from src import *

# Initialize handles
sftp = SFTPHandle(*sftp_credentials)
azure = AzureBlobStorageHandle(*azure_credentials)

# Send multiple files from SFTP to Azure Blob Storage
files = ("/home/ez/minecraft.exe", "/home/ez/selfie.png")
destination = "transfer/"
Transfer(source=sftp, destination=azure).files(files).to(destination).execute()

# Single file from SFTP to Azure Blob Storage
Transfer(source=sftp, destination=azure).file("/home/ez/selfie.png").to("received/image.png").execute()

# Single file (this time in opposite direction) from Azure Blob Storage to SFTP
Transfer(source=azure, destination=sftp).file("received/image.png").to("/home/ez/selfie.png").execute()
```

## Supported Services

- SFTP
- Azure Blob Storage

For now, just two of them. Expect more in near future...

Feel free to suggest, what I should cover next.


<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->

## Contact

Michal Broton - [LinkedIn](https://linkedin.com/in/broton)

Project Link: [https://github.com/mbroton/ez-transfer](https://github.com/mbroton/ez-transfer)
