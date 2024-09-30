# Data Watchdog

<img src="assets/img/logo.png" alt="logo page">

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

Data Watchdog is a tool built to find and classify Personally Identifiable Information (PII) like names, emails, Aadhaar numbers, and PAN numbers in different types of data storage. It works with databases like MySQL and cloud services like Google Cloud and Amazon S3. The tool supports various file types, including unstructured files (such as `.txt`, `.log`, `.jpg`, `.png`, `.jpeg`, `.pdf`, `.mp3`, `.mp4`) and structured files (such as `.csv`). 

**Objective**: Storing personal data comes with risks, and businesses need to follow rules to protect it. Data Watchdog helps companies find and classify personal data in their systems, making sure they follow data privacy laws like GDPR and CCPA, and reduce the risk of data breaches.

**Features**: 

1. Data Ingestion and Continuous Integration: Efficiently handles data from multiple sources, including Amazon AWS Cloud and SQL databases, as well as various file formats such as text files, log files, images, CSVs, and PDFs. Once configured, it continuously integrates and updates data fetched from the cloud.

2. PII Detection: Utilizes machine learning and advanced techniques to identify personal identifiable information (PII). Provides a comprehensive list of detected PII across various file types.

3. Drilldown: Calculates a risk score based on the type of detected PII. Classifies data into categories and buckets, allowing users to view information at different levels of granularity.

4. Data Visualization: Offers analytics related to detected PII, including metrics such as mean risk per file, mean risk per file type, total PII counts per file, and identification of the riskiest PII elements.

## Demo

https://github.com/user-attachments/assets/597ad48b-8e24-47e1-8d08-26b8420f3aae

## Methodology

We primarily deal with 6 types of files, which are Text Files (`.txt`, `.log`, `.docx`), Image Files (`.png`, `.jpg`, `.jpeg`), PDF Files (`.pdf`), CSV Files (`.csv`), Audio Files (`.mp3`) and Video Files(`.mp4`). Details about each PII extraction process can be found <a href="model/README.md">here</a>

### High Level Design

<img src="assets/img/flowchart.png" alt="flowchart">

### Sequence Diagram

<img src="assets/img/sequence diagram.png" alt="sequence diagram">

### API Contract
API Contract for the project can be found <a href="api_contract.yaml">here</a>

## Tech Stack

- ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

- ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

- ![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)

- ![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

- ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

- ![Hugging Face](https://img.shields.io/badge/Hugging%20Face-FFD43B?style=for-the-badge&logo=hugging-face&logoColor=white)

## File Structure
```
👨‍💻Data Watchdog
 ┣ 📂assets
 ┃ ┣ 📂demo
 ┃ ┣ 📂img          
 ┃ ┣ 📂temp                            // Sample files for testing
 ┃ ┣ 📂results                         // Output
 ┃ ┣ 📄problem-statement.pdf
 ┣ 📂client                            // Frontend        
 ┃ ┣ 📂static    
 ┃ ┣ 📂templates    
 ┃ ┃ ┣ 📄home.html
 ┃ ┃ ┣ 📄configure.html
 ┃ ┃ ┣ 📄dashboard.html 
 ┃ ┃ ┣ 📄view.html                           
 ┣ 📂model                                      
 ┃ ┣ 📄detect.py                       // Core functionality
 ┃ ┣ 📄utils.py 
 ┃ ┣ 📄analytics.py
 ┃ ┣ 📄postprocess.py
 ┃ ┣ 📄main.py
 ┃ ┣ 📄requirements.txt
 ┃ ┣ 📄README.md            
 ┣ 📂server                            // Backend 
 ┃ ┣ 📂archive  
 ┃ ┣ 📄app.py  
 ┃ ┣ 📄requirements.txt 
 ┣ 📄api_contract.yaml
 ┣ 📄data-watchdog-ppt.pptx  
 ┣ 📄Configure.md   
 ┣ 📄README.md
``` 

## Getting Started

### Installation

Clone the project by typing the following command in your Terminal/CommandPrompt

```
git clone git@github.com:PritK99/Data-Watchdog.git
```
Navigate to the Data Watchdog folder

```
cd Data-Watchdog
```

#### Usage

Create a virtual environment to install all the dependencies

```
python -m venv data-watchdog
```

Activate the virtual environment

For Windows: ```data-watchdog\Scripts\activate```

For Linux: ```source data-watchdog/bin/activate```

Install all the required dependencies

Open a new terminal in root folder and navigate to the server folder

```
cd server/
```

Install all the required dependencies

```
pip install -r requirements.txt
```

> **Note** <br>
>
> <i>Path to `poppler` and `pytesseract` are required in `utils.py` to perform pdf to image conversion and OCR respectively.
>
> For `poppler` refer <a href="https://github.com/oschwartz10612/poppler-windows/releases/tag/v24.07.0-0">here</a>.
>
> For `pytesseract` refer <a href="https://tesseract-ocr.github.io/tessdoc/Installation.html">here</a>.
>
> Please replace the paths in `utils.py` with your paths.</i>
>
> In addition to this, we require `ffmpeg` to deal with multimedia files such as audio and video. For the installation, please refer this <a href="https://www.youtube.com/watch?v=JR36oH35Fgg">YouTube video</a>

Once all the above steps are completed, run the createdatabase.py script using the following command in the terminal in `server` directory:

```
python app.py  
```

Running the server will load the frontend at `http://localhost:5000/`

> **Note** <br>
><i>The configuration page will require the configurations of SQL or Cloud that we want to analyze. For demo purpose we are using `PostgreSQL` using Render and `LocalStack` which allows us to simulate AWS cloud environment locally. For configuring these, steps are provided in <a href="Configure.md">Configure markdown file</a>.</i>

## Screenshots of the Website

### Home Page

<img src="assets/img/home page 1.png" alt="home page">

<img src="assets/img/home page 2.png" alt="home page">

### Configuration Page

<img src="assets/img/config page.png" alt="config page">

### Analytics and Dashboard

<img src="assets/img/dashboard.png" alt="dashboard page">

### Drilldown Page

<img src="assets/img/drilldown.png" alt="drilldown page">

### Output File

<img src="assets/img/download.png" alt="output.csv">

## Contributors

- [Kavan Gandhi](https://github.com/KGan31)
- [Prit Kanadiya](https://github.com/PritK99)

## License
[MIT License](https://opensource.org/licenses/MIT)
