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

   - **'.gitignore`**: This file is just a file to avoid tracking files that we don't want to see in the repository, for example __pycache__, .DS_Store and some others.

### Technologies Used:

- Mention any frameworks, libraries, or tools used in your project (like Flask, SQLite, Jinja, etc.).

### Contributions:

- If you're open to contributions, provide guidelines on how others can contribute to your project.
- Provide contact information or steps for submitting pull requests or issues.

### Acknowledgements

This project utilizes BLIP (Bootstrapping Language-Image Pre-training), an innovative model for unified vision-language understanding and generation. I extend my gratitude to the authors Junnan Li, Dongxu Li, Caiming Xiong, and Steven Hoi for their significant contributions to the field of Computer Vision and Pattern Recognition. Their work has been instrumental in the development of this project.

For more details on BLIP, please refer to their paper:

Junnan Li, Dongxu Li, Caiming Xiong, and Steven Hoi. "BLIP: Bootstrapping Language-Image Pre-training for Unified Vision-Language Understanding and Generation." arXiv preprint arXiv:2201.12086 (2022). DOI: [10.48550/ARXIV.2201.12086](https://doi.org/10.48550/arxiv.2201.12086). URL: [https://arxiv.org/abs/2201.12086](https://arxiv.org/abs/2201.12086).


---

Remember to replace placeholders (like YOUR PROJECT TITLE, URL HERE, TODO) with your actual project information. If you don't have a video demo, you can omit that part or add it later when you have one. 

The README file is important as it gives visitors and potential users an overview of your project, how to set it up, and how to use it. It's also an excellent place to showcase your work and explain your development process.
