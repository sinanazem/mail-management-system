import streamlit as st
from src.utils.database import DatabaseManager
import os

import base64
from PIL import Image
import wikipedia
from streamlit_searchbox import st_searchbox



db = DatabaseManager(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
    )




def main():
    st.image("https://t4.ftcdn.net/jpg/05/67/36/21/360_F_567362151_3KEKqSXAHbTAgEzKW5IDrta5TZvsJlAL.png")
    

    # Add new profile
    st.markdown("### 🧑‍💻 Add New Profile")
    with st.expander(f"User Information Form"):

        with st.form("user_form"):
            profile_image = st.file_uploader("Upload Profile Image", type=["jpg", "jpeg", "png"])
            col1, col2 = st.columns(2)
            
            with col1:
                first_name = st.text_input("First Name")
                profession = st.text_input("Profession")
            
            with col2:
                last_name = st.text_input("Last Name")
                email = st.text_input("Email")
            
            about = st.text_area("About")
            col1, col2 = st.columns(2)
            with col1:
                twitter = st.text_input("Twitter URL")
                github = st.text_input("GitHub URL")
                linkedin = st.text_input("LinkedIn URL")
            
            with col2:
                personal_website = st.text_input("Personal Website URL")
                instagram = st.text_input("Instagram URL")

            submitted = st.form_submit_button("Submit")
            
            if submitted:
                social_media = {
                    "twitter": twitter,
                    "github": github,
                    "linkedin": linkedin,
                    "personal_website": personal_website,
                    "instagram": instagram
                }

                # Insert user into the database without the image path first
                profile_id = db.add_profile(first_name=first_name,
                                         last_name=last_name,
                                         profession=profession,
                                         email=email,
                                         about=about,
                                         twitter=twitter,
                                         github=github,
                                         linkedin=linkedin,
                                         personal_website=personal_website,
                                         instagram=instagram,
                                         profile_image_path="")

                # Save the profile image using user_id in the file path
                if profile_image is not None:
                    
                    # Define folder to store profile images
                    UPLOAD_FOLDER = 'profile_images'

                    # Create folder if it doesn't exist
                    if not os.path.exists(UPLOAD_FOLDER):
                        os.makedirs(UPLOAD_FOLDER)
                    # Define the image filename and file path (use the user_id in the name)
                    file_extension = profile_image.name.split('.')[-1]
                    image_filename = f"{profile_id}.{file_extension}"
                    image_path = os.path.join(UPLOAD_FOLDER, image_filename)

                    # Open and save the image
                    image = Image.open(profile_image)
                    image.save(image_path)

                    # Update the user's profile image path in the database
                    db.update_profile(profile_id=profile_id, profile_image_path=image_path)

                    st.success(f"User added with ID: {profile_id}")

#     # View and delete existing profiles

    st.markdown("### 📇 Existing Profiles")

        # Sample profile data
    profile_data = db.get_all_profiles()


    num_cols = 3
    cols = st.columns(num_cols)
    for idx, raw_profile in enumerate(profile_data):
        with cols[idx % num_cols]:
            profile = {
                "first_name": raw_profile[1],
                "last_name": raw_profile[2],
                "profession": raw_profile[3],
                "email": raw_profile[4],
                "about": raw_profile[5],
                "twitter": raw_profile[6],
                "github": raw_profile[7],
                "linkedin": raw_profile[8],
                "personal_website": raw_profile[9],
                "instagram": raw_profile[10],
                "profile_image_path": raw_profile[11] if os.path.exists(raw_profile[11]) else "/mnt/c/Users/user/OneDrive/Desktop/email-dashboard/profile_images/user-profile.jpg"
            }
            display_profile_card(profile)


def image_to_base64(image_path):
        """
        Convert an image file to base64.
        """
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
    
    
def display_profile_card(profile):
    # HTML and CSS for profile card
    card_html = f"""
    <style>
    .profile-card {{
        width: 100%;
        max-width: 230px;
        margin: 0 auto;
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        transition: 0.3s;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        height: 350px;  /* Force same height for all cards */
    }}
    .profile-card:hover {{
        box-shadow: 0 0 20px rgba(0,0,0,0.2);
    }}
    .profile-card img {{
        border-radius: 50%;
        width: 100px;
        height: 100px;
        object-fit: cover;
    }}
    .social-icons a {{
        margin: 5px;
        text-decoration: none;
        color: gray;
        font-size: 20px;
    }}
    .social-icons a:hover {{
        color: #007bff;
    }}
    </style>
    <div class="profile-card">
        <img src="data:image/png;base64,{image_to_base64(profile['profile_image_path'])}" alt="Profile Image">
        <h6>{profile['first_name']} {profile['last_name']}</h6>
        <h7>{profile['profession']}</h7>
        <p>{profile['about']}</p>
        <div class="social-icons">
    """
    social_media_links = {
        "twitter": '<i class="fab fa-twitter"></i>',
        "github": '<i class="fab fa-github"></i>',
        "linkedin": '<i class="fab fa-linkedin"></i>',
        "personal_website": '<i class="fas fa-globe"></i>',
        "instagram": '<i class="fab fa-instagram"></i>'
    }
    for key, icon in social_media_links.items():
        if profile.get(key):
            card_html += f'<a href="{profile[key]}" target="_blank">{icon}</a>'
    
    card_html += """
        </div>
    </div>
    """

    # Include the Font Awesome link
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
        """,
        unsafe_allow_html=True
    )

    # Display the HTML card
    st.markdown(card_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
