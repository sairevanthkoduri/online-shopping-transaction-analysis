# Setup checklist

- [ ] Install Python 3.10 or newer
- [ ] Install and start MySQL Server
- [ ] Open the folder in VS Code
- [ ] Create virtual environment and install `requirements.txt`
- [ ] Copy `.env.example` to `.env`
- [ ] Set your MySQL credentials in `.env`
- [ ] Run `python setup_database.py`
- [ ] Run `streamlit run app.py`

If `mysql.connector.errors.AccessDeniedError` appears, verify the MySQL username/password in `.env`.
If the app says it cannot connect, make sure the MySQL service is running.
