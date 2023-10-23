"""

Config file for Streamlit App

"""

from member import Member


TITLE = "My Awesome App"

TEAM_MEMBERS = [
    Member(
        name="John Doe",
        linkedin_url="https://www.linkedin.com/in/charlessuttonprofile/",
        github_url="https://github.com/charlessutton",
    ),
    Member("Jane Doe"),
]

PROMOTION = "Promotion Bootcamp Data Scientist - April 2021"
