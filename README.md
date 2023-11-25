# splunk-sdk

__Description:__ Splunk SDK Extension of Splunk Library

Sample Usage with ``.env`` configured.

```python
from dotenv import load_dotenv
import os

from splunksdk.splunk import SplunkApi

load_dotenv()

# Create a splunk instance
s = SplunkApi(**os.environ)

# Display available collections
s.KVstore.collections 

# Run a search

s.Search.start_search(query="|inputlookup filename")

# Get Search
s.Search.get_results()

# Jobs are stored in attributes
s.Search.search_resp
s.Search.csv_results
s.json_cols_results
```
