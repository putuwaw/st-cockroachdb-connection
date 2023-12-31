import streamlit as st

st.title("How to Build CockroachDB Connection")

"""
1. First you need to have a minimal Streamlit app like this:

```
.
├── .streamlit/
│   └── secrets.toml
├── cockroachdb_connection/
│   ├── __init__.py
│   ├── connection.py
│   └── util.py
└── app.py
```

2. Don't forget to install `streamlit` and `psycopg` package.

```bash
pip install streamlit>=1.28.0 "psycopg[binary]"

```

3. Before we make the connection, we need to create a utility function in `util.py` to get the parameters from `kwargs`.

```py
def extract_conn_kwargs(params: set, target: dict) -> dict:
    result = {}
    for p in params:
        if p in target:
            result[p] = target[p]
    return result
```

4. Then we will work in the `connection.py` file and import the modules:

```py
from streamlit.connections import BaseConnection
from streamlit.errors import StreamlitAPIException
from streamlit.runtime.caching import cache_data
from psycopg import Connection, Cursor
from .util import extract_conn_kwargs
from collections import ChainMap
import pandas as pd
import psycopg
import certifi
```

5. We also need to create variabel that contains all connection parameters and required connection parameters.

```py
_ALL_CONNECTION_PARAMS = {
    "url",
    "dialect",
    "username",
    "password",
    "host",
    "port",
    "database",
}

_REQUIRED_CONNECTION_PARAMS = {"username", "password", "host", "database"}
```

6. Than we create a new connection class called `CockroachDBConnection` that extends Streamlit's `BaseConnection`

```py
class CockroachDBConnection(BaseConnection[Connection]):
```

7. Add a `_connect()` method that sets up and returns the underlying connection object.

```py
def _connect(self, **kwargs) -> Connection:
    # get connections params from keyword args
    kwargs_params = extract_conn_kwargs(_ALL_CONNECTION_PARAMS, kwargs)

    # get params from secret
    secret_params = self._secrets.to_dict()

    # all connection params
    conn_params = ChainMap(kwargs_params, secret_params)

    # check if connection params are empty
    if not len(conn_params):
        raise StreamlitAPIException(
            "Missing CockroachDB connection configuration. "
            "Did you forget to set this in `secrets.toml` or as kwargs to `st.connection`?"
        )

    url: str = ""
    if "url" in conn_params:
        url = conn_params["url"]
    else:
        # check missing req params
        for i in _REQUIRED_CONNECTION_PARAMS:
            if i not in conn_params:
                raise StreamlitAPIException(
                    f"Missing CockroachDB required connection parameter: {i}"
                    f"Did you forget to set {i} in `secrets.toml` at `[connections.<name>]` section or as kwargs to `st.connection`?"
                )

        # construct url
        dialect = conn_params["dialect"] if "dialect" in conn_params else "postgresql"
        port = conn_params["port"] if "port" in conn_params else "26257"
        username = conn_params["username"]
        password = conn_params["password"]
        host = conn_params["host"]
        database = conn_params["database"]
        sslmode = "verify-full"

        url = f"{dialect}://{username}:{password}@{host}:{port}/{database}?sslmode={sslmode}"
    
    # return connection object
    return psycopg.connect(url, sslrootcert=certifi.where())
```

8. Add a `_cursor` method to get the underlying connection object.

```py
def cursor(self) -> Cursor:
    return self._instance.cursor()

```
9. Add a `query` method to execute queries to the database.

```py
def query(self, query: str, ttl: int = 3600, **kwargs) -> pd.DataFrame:
    @cache_data(ttl=ttl)
    def _query(query: str, **kwargs) -> pd.DataFrame:
        cursor = self.cursor()
        cursor.execute(query, **kwargs)
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return pd.DataFrame(result, columns=columns)
    return _query(query, **kwargs)
```

10. Add other methods like `execute`, `commit`, `reset` to execute queries and reset the connection.

```py
def execute(self, query: str) -> None:
    cursor = self.cursor()
    cursor.execute(query)

def commit(self) -> None:
    self._instance.commit()

def reset(self) -> None:
    return super().reset()
```

11. Now go to file `__init__.py` and import the connection class.

```py
from cockroachdb_connection.connection import CockroachDBConnection
```

12. Congratulations, now you can import the connection class in `app.py` and use it to query. 
Remember to add the parameter to `secrets.toml` in `[connections.<name>]` section. You also can pass it as a keyword argument to `st.connection`.
"""
