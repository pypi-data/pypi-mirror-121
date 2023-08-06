### CCS

Configuration control system

#### Installation

```
pip3 install occson
```

#### Example

```python
from occson.document import Document

document = Document("ccs://.env", "<ACCESS_TOKEN>", "<PASSPHRASE>")
print(document.download())
print(document.upload("A=1\nB=2", True))
```
