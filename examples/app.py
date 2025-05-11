import streamlit as st
from st_pages import Page, show_pages


st.set_page_config(
    page_title='Example App',
    page_icon='🏠'
)

show_pages(
    [
        Page("app.py", "Home", "🏠"),
        Page("pages/information.py", "Information", "👀"),
        Page("pages/example.py", "Example", "💡")
    ]
)


st.title("CockroachDB Connection")

tab1, tab2 = st.tabs([
    "🚀 With st.connection",
    "🐢 How it worked before"
])

with tab1:
    st.markdown(
        "With `st.connection` you can connect to a CockroachDB database and query it directly from Streamlit.")
    st.code(
        """
        import streamlit as st
        from st_cockroachdb_connection import CockroachDBConnection

        conn = st.connection("cockroachdb", type=CockroachDBConnection)
        df = conn.query("SELECT price FROM items")
        st.dataframe(df)
        """
    )


with tab2:
    st.markdown(
        "Compared to the old way of doing it, which required to write more code.")
    st.code(
        """
        import streamlit as st
        import pandas as pd
        import psycopg

        @st.cache_resource
        def init_connection():
            return psycopg.connect(st.secrets["connections"]["cockroachdb"]["url"])

        conn = init_connection()

        @st.cache_data(ttl=600)
        def run_query(query):
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                return pd.DataFrame(result, columns=columns)

        df = run_query("SELECT price FROM items;")
        st.dataframe(df)
        """
    )

st.subheader("What's next?")
st.markdown(
    """
    - Learn how to build the connection in the [Information](https://experimental-connection-hackathon.streamlit.app/Information) page.
    - See the functional demo in the [Example](https://experimental-connection-hackathon.streamlit.app/Example) page.
    - Learn more in the [API docs](https://docs.streamlit.io/library/api-reference/connections).
    """
)
