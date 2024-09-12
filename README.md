# Data Watchdog

## Table of Contents

- [Project](#data-watchdog)
  - [Table of Contents](#table-of-contents)
  - [About The Project](#about-the-project)
  - [Demo](#demo)
  - [Methodology](#methodology)
  - [Tech Stack](#tech-stack)
  - [File Structure](#file-structure)
  - [Getting started](#getting-started)
  - [Screenshots of Website](#screenshots-of-the-website)
  - [Contributors](#contributors)
  - [License](#license)

## About The Project

Data Watchdog is a tool built to find and classify Personally Identifiable Information (PII) like names, emails, Aadhaar numbers, and PAN numbers in different types of data storage. It works with databases like MySQL and cloud services like Google Cloud and Amazon S3. The tool supports various file types, including unstructured files (such as `.txt`, `.log`, `.jpg`, `.pdf`) and structured files (such as `.csv`). 

**Objective**: Storing personal data comes with risks, and businesses need to follow rules to protect it. Data Watchdog helps companies find and classify personal data in their systems, making sure they follow data privacy laws like GDPR and CCPA, and reduce the risk of data breaches.

**Features**: 

1. Data Ingestion: Handles data from multiple file types like text files, log files, images, CSVs, PDFs etc

2. PII Detection: Detects personal data using machine learning and other techniques.

3. Risk Assessment: Calculates a risk score based on the type and volume of detected PII.

4. Data Visualization: Shows the analytics associated with detect PII.

## Demo

## Methodology

<img src="assets/img/flowchart.png" alt="flowchart">

We primarily deal with 4 types of files, which are Text Files (`.txt`, `.log`), Image Files (`.png`, `.jpg`, `.jpeg`), PDF Files (`.pdf`) and CSV Files (`.csv`). Details about each PII extraction process can be found <a href="model/README.md">here</a>

## Tech Stack

- ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

- ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

- ![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)

- ![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

- ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

- ![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD43B?style=for-the-badge&logo=hugging-face&logoColor=white)

## File Structure
```
👨‍💻Legal-Documentation-Assistant
 ┣ 📂assets                            // Contains all the reference gifs, images
 ┣ 📂client                            // Frontend        
 ┃ ┣ 📂src                                      
 ┃ ┃ ┣ 📂components  
 ┃ ┃ ┃ ┣ 📄Chat.jsx
 ┃ ┃ ┣ 📄about.jsx
 ┃ ┃ ┣ 📄Faq.jsx
 ┃ ┃ ┣ 📄Home.jsx
 ┃ ┃ ┣ 📄InputForm.jsx
 ┃ ┃ ┣ 📄LoginPage.jsx
 ┃ ┣ 📂public 
 ┃ ┃ ┣ 📄index.html
 ┣ 📂model                             // Standalone model         
 ┃ ┣ 📄similarity.py                   // Based on Cosine Similarity
 ┃ ┣ 📄bot.py    
 ┃ ┣ 📄chat.py                         // To chat with the standalone model
 ┃ ┣ 📄model.py                        // Based on Bag of Words
 ┃ ┣ 📄train.py                        
 ┃ ┣ 📄dataset.py 
 ┃ ┣ 📄util.py   
 ┃ ┣ 📄trained_model.pth
 ┃ ┣ 📄intents.json                    // Dataset 
 ┣ 📂server                            // Backend 
 ┃ ┣ 📂docs  
 ┃ ┃ ┣ 📄localfile.docx
 ┃ ┃ ┣ 📄Output2.docx
 ┃ ┣ 📄app.py 
 ┃ ┣ 📄createdatabase.py  
 ┃ ┣ 📄requirements.txt      
 ┣ 📄README.md
``` 

## Getting Started

### Installation

Clone the project by typing the following command in your Terminal/CommandPrompt

```
git clone https://github.com/PritK99/Legal-Documentation-Assistant.git
```
Navigate to the Legal Documentation Assistant folder

```
cd Legal-Documentation-Assistant
```

#### Frontend

Open a new terminal in root folder and navigate to the client folder

```
cd client/
```

Install all the required dependencies

```
npm i
```

To run the frontend

```
npm start
```

Once the above command is executed, the frontend will be running at ```localhost:3000```. You can visit http://localhost:3000/ to view the website.

#### Backend

Open a new terminal in root folder and navigate to the server folder 

```
cd server
```

Create a virtual environment to install all the dependencies

```
python -m venv docbuddy
```

Activate the virtual environment

For Windows: ```docbuddy\Scripts\activate```

For Linux: ```source docbuddy/bin/activate```

Install all the required dependencies

```
pip install -r requirements.txt
```

To create a database on render and creating a environment file, follow the given steps

1. Visit the [website](https://render.com/) and create an account or sign in. 
2. Next, choose a new service as PostgreSQL to create a new database service. 
3. Give an appropriate name to the database and the instance name.
4. Select <b>Free</b> option in the Instance type and hit <b>Create Database</b> button at the bottom.

A new empty PostgreSQL database service will then be created. You can view all the services on your Render Dashboard.
> **Note** <br>
> The PostgreSQL database service will remain free on render only upto 3 months.


Next, create a .env file containing the credentials of your database. Sample .env file looks like:
```
DATABASE_HOST=your_database_host
DATABASE_NAME=your_database_name
DATABASE_USER=your_database_username
PASSWORD=your_database_password
DATABASE_PORT=your_database_port
```

> **Note** <br>
> ```DATABASE_HOST``` in ```.env``` should be of form ```<Hostname>.<region>-postgres.render.com```. For example, if the region of database is ```Oregon (US West)```, then hostname can be ```<Hostname>.oregon-postgres.render.com```
  

You can get all this database credentials by visiting the PostgreSQL database service you created on your render dashboard.

Once the .env file is setup, next run the createdatabase.py script using the following command in the terminal:
```
python server/createdatabase.py  
```

Running the createdatabase.py script will create the entire database for you.

> **Note** <br>
> If you want to create the PostgreSQL database on your local device instead of hosting on render, you are free to do so. But, you need to change the .env file accordingly.

To run the backend

```
python app.py
```

## Screenshots of the Website

## Contributors

- [Kavan Gandhi](https://github.com/KGan31)
- [Prit Kanadiya](https://github.com/PritK99)

## License
[MIT License](https://opensource.org/licenses/MIT)