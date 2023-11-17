from streamlit.connections import BaseConnection
from streamlit.errors import StreamlitAPIException
from streamlit.runtime.caching import cache_data
from psycopg import Connection, Cursor
from .util import extract_conn_kwargs
from collections import ChainMap
import pandas as pd
import psycopg
import certifi

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


class CockroachDBConnection(BaseConnection[Connection]):
    """
    Description: The `_connect` function is a utility function designed to establish a connection to a CockroachDB
    database. It provides a convenient way to connect to the database and can be used as a building block for
    interacting with the CockroachDB in Python applications.
    """

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
                        f"Did you forget to set {i} in `secrets.toml` at `[connections.<name>]` section or as kwargs "
                        f"to `st.connection`?"
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

    def cursor(self) -> Cursor:
        return self._instance.cursor()

    def query(self, query: str, ttl: int = 3600, **kwargs) -> pd.DataFrame:
        @cache_data(ttl=ttl)
        def _query(query: str, **kwargs) -> pd.DataFrame:
            cursor = self.cursor()
            cursor.execute(query, **kwargs)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return pd.DataFrame(result, columns=columns)
        return _query(query, **kwargs)

    def execute(self, query: str) -> None:
        cursor = self.cursor()
        cursor.execute(query)

    def commit(self) -> None:
        self._instance.commit()

    def reset(self) -> None:
        return super().reset()
