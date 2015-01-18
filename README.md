Kounta
------

Python client library for Kounta.com

```python
from kounta.client import BasicClient

kounta = BasicClient('client_id', 'client_secret')
for site in kounta.company.sites:
    print site.name
```

**Only basic authentication is currently supported.**
