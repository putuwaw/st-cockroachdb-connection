# experimental-connection

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![CockroachDB](https://img.shields.io/badge/CockroachDB-6933FF?style=for-the-badge&logo=Cockroach%20Labs&logoColor=white)
![LICENSE](https://img.shields.io/github/license/putuwaw/experimental-connection?style=for-the-badge)
![BUILD](https://img.shields.io/github/actions/workflow/status/putuwaw/experimental-connection/streamlit.yml?style=for-the-badge)

Experimental Connection to CockroachDB using Streamlit.

## Features 🚀

With this apps you can connect to CockroachDB easily using `st.experimental_connection` in just few lines of code. You can also execute SQL queries and see the result in more efficient way.

## Prerequisites 📋

- Python 3.10 or higher
- Streamlit 1.25.0 or higher
- Psycopg 3.0 or higher

## Installation 🛠

- Clone the repository:

```bash
git clone https://github.com/putuwaw/experimental-connection.git
```

- Install the packages:

```bash
pip install -r requirements.txt
```

- Set up secret for database connection:

```bash
cp .streamlit/secret.example.toml .streamlit/secrets.toml
```

- Run the application:

```bash
streamlit run 🏠_Home.py
```

## License 📝

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
