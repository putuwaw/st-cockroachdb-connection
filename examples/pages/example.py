import streamlit as st

st.title("Functional Demo")
st.write("Now lets use the connection class to query the database.")

with st.echo():
    from st_cockroachdb_connection import CockroachDBConnection
    conn = st.connection("cockroachdb", type=CockroachDBConnection)

    # create table
    conn.execute("CREATE TABLE IF NOT EXISTS items (name STRING NOT NULL, price DECIMAL(10,2) NOT NULL, count INT NOT NULL);")

    # delete existing data
    conn.execute("DELETE FROM items;")

    # insert into table
    conn.execute("INSERT INTO items (name, price, count) VALUES ('jeans', 23, 50), ('laptop', 499.90, 35), ('camera', 399, 25);")

    # commit transaction
    conn.commit()

st.write("Let's see what's in the table and display it in the form of a dataframe!")

with st.echo():
    df = conn.query("SELECT * FROM items")
    st.dataframe(df)

conn.reset()
