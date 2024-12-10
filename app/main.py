# # main.py
# import streamlit as st
# from utils.database import Database

# # Initialize database
# db = Database()
# db.setup_database()

# # Main app
# def main():
#     st.set_page_config(
#         page_title="IPO Monitor",
#         page_icon="📈",
#         layout="wide"
#     )
    
#     # Main page navigation handled by Streamlit pages

# if __name__ == "__main__":
#     main()

# app/main.py
import streamlit as st
from utils.database import Database

def main():
    st.set_page_config(
        page_title="IPO Monitor",
        page_icon="📈",
        layout="wide"
    )
    
    # Initialize database
    db = Database()
    
    # Main page will be handled by Streamlit pages

if __name__ == "__main__":
    main()