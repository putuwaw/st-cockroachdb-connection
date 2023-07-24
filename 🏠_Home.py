import streamlit as st

st.set_page_config(
    page_title='Connections Hackaton',
    page_icon='🏠'
)

st.title("CockroachDB Connection")

tab1, tab2 = st.tabs([
    "🚀 With st.experimental_connection",
    "🐢 How it worked before"
])

with tab1:
    st.markdown(
        "With `st.experimental_connection` you can connect to a CockroachDB database and query it directly from Streamlit.")
    st.code(
        """
        import streamlit as st
        from cockroachdb_connection import CockroachDBConnection

        conn = st.experimental_connection("cockroach", type=CockroachDBConnection)
        df = conn.query("SELECT price FROM items")
        st.dataframe(df)
        """
    )


with tab2:
    st.markdown(
        'Compared to the old way of doing it, which required to write more code.')
    st.code(
        """
        import streamlit as st
        import pandas as pd
        import psycopg

        @st.cache_resource
        def init_connection():
            return psycopg.connect(st.secrets["connections"]["cockroach"]["url"])

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
