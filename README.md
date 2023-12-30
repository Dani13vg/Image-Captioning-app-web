# PIXTALES: The Image Captioning app web

<img src="https://raw.githubusercontent.com/Dani13vg/Image-Captioning-app-web/main/static/Pixtales.jpeg" alt="PIXTALES: The Image Captioning app web">

#### Video Demo: [URL HERE]

#### Description:

PIXTALES is an innovative web application designed to revolutionize the way we interact with images. Utilizing cutting-edge AI and deep learning technologies, PIXTALES provides users with the unique ability to generate descriptive captions for their uploaded images.

## Key Features:

- **Image Captioning**: Upload any image, and PIXTALES will use advanced AI algorithms to analyze and generate a relevant, descriptive caption. This feature is perfect for enhancing understanding of visual content, particularly useful for visually impaired users.

- **User-Friendly Interface**: Designed with simplicity in mind, our intuitive interface ensures a seamless user experience. Upload images effortlessly and receive instant captions.

- **History Tracking**: Users can view their history of uploaded images along with their generated captions, providing a convenient way to revisit past uploads.

- **Secure and Private**: We prioritize user privacy and data security, ensuring that your images and information are handled with the utmost care.


### How to Run the Application:

1. **Setup Environment**: 
   - You will need to have an environment with python installed(I used version 3.11.5) that must contain the requirements list in the `requirements.txt` file. Some of the requirements are `Flask`, `PyTorch`, `SQL`, `Pillow`, `transformers` and other dependencies.
   - I recommend using a new environment using only the requirements listed so that there are no conflicts between packages.

2. **Running the App**: 
   - Once in the directory where the app.py is (the root of this repository), you can use `flask run` or `python app.py` to run the web app.
   - The previous command will show you in the terminal a URL that you can click on to see the web app.

3. **Content of the directory**: 

In this directory you will find the following elements:

   - **`app.py`**: This is the main script where the application is programmed. It controls everything that happens on the web pages and within the databases.

   - **`helpers`**: This file contains some auxiliary functions to use in the `app.py`.

   - **`model.py`**: This file contains the function used to generate captions for the images and code to test the model.

   - **`users.db`**: This is the database where we store the information of the users and their images with the corresponding captions.

   - **`templates`**: This is a folder with the different html files used for the web app.

   - **`static`**: This is a folder with the `styles.css` file containing the CSS configurations to enhance the appearance of the web and some images used for the design and also to test the app.

   - **`.gitignore`**: This file is just a file to avoid tracking files that we don't want to see in the repository, for example __pycache__, .DS_Store and some others.

## Technologies Used

PIXTALES leverages a range of modern technologies and frameworks to provide a seamless and efficient user experience. Below is a list of the key technologies employed in this project:

- **Flask**: A lightweight WSGI web application framework in Python, used for building the web server and handling HTTP requests.

- **SQLite**: A C-language library that implements a small, fast, self-contained, high-reliability, full-featured, SQL database engine. It's used for storing user data, including image paths and generated captions.

- **BLIP Model (Salesforce)**: Utilized for image captioning, the BLIP (Bootstrapping Language-Image Pre-training) model from Salesforce represents the state-of-the-art in AI for understanding and generating language descriptions of images.

- **HTML/CSS**: Used for structuring and styling the web application's frontend.

- **JavaScript**: Employed for adding interactive elements to the web pages for an enhanced user experience.

- **Bootstrap**: A front-end framework used to create modern, responsive layouts.

- **Git**: For version control, ensuring efficient management of the codebase and collaboration.

Each of these technologies contributes to the robust functionality of PIXTALES, making it a powerful tool for image captioning and an exemplar of the capabilities of modern web applications.

### Web Usage:

Once entered into the main page of the web app you will find the option to register and login (since you are not registered, you should go to the registered option). You will always see some options in the navigation bar at the top of the page those options are the following:

- **Home**: This option redirects you to the main page.

- **Usage**: This option will provide you some instructions about how to use the web app.

- **Contact Us**: This option will let you some information to know how to contact me.

- **Captioning**: Once this option is selected, you will be prompted for a file (an image in any of this formats: 'png', 'jpg', 'jpeg', 'gif') to generate a caption for it. The user must be log in to access this option.

- **History**: This option leads you to a page where you can see all the images you has uploaded with the corresponding caption.

- **Log out**: This option logs the user out and redirects him to the home page. This options only appears after the user has log in.



### Contributions:

- If you're open to contributions, provide guidelines on how others can contribute to your project.
- Provide contact information or steps for submitting pull requests or issues.

### Acknowledgements

This project utilizes BLIP (Bootstrapping Language-Image Pre-training), an innovative model for unified vision-language understanding and generation. I extend my gratitude to the authors Junnan Li, Dongxu Li, Caiming Xiong, and Steven Hoi for their significant contributions to the field of Computer Vision and Pattern Recognition. Their work has been instrumental in the development of this project.

For more details on BLIP, please refer to their paper:

Junnan Li, Dongxu Li, Caiming Xiong, and Steven Hoi. "BLIP: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation." arXiv preprint arXiv:2201.12086 (2022). DOI: [10.48550/ARXIV.2201.12086](https://doi.org/10.48550/arxiv.2201.12086). URL: [https://arxiv.org/abs/2201.12086](https://arxiv.org/abs/2201.12086).


---


