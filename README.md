# Ethiopian Medical Data Warehouse Project

## Overview

As a data engineer at Kara Solutions, you are tasked with building a data warehouse that will store and analyze data related to Ethiopian medical businesses. This data will be scraped from web sources and Telegram channels. The warehouse must be scalable, efficient, and capable of handling data scraped from various platforms, including Telegram. You will also integrate object detection capabilities using YOLO (You Only Look Once) to enhance data collection and analysis.

The main goal of the project is to create a centralized data warehouse that makes it easier to analyze trends, patterns, and correlations within the data, helping decision-makers gain valuable insights. The project will also include efficient querying and reporting capabilities to provide actionable intelligence.

## Project Breakdown

The project consists of the following key tasks:

1. **Data Scraping and Collection Pipeline**
2. **Data Cleaning and Transformation**
3. **Object Detection Using YOLO**
4. **Expose Collected Data Using FastAPI**

---

### Task 1: Data Scraping and Collection Pipeline

#### Telegram Scraping

The first task is to scrape data from relevant Telegram channels. You will be using the Telegram API or custom Python scripts to extract data from these channels. Some of the key channels include:

- DoctorsET
- Chemed Telegram Channel
- Yetenaweg
- EAHCI
- Additional channels can be found at ET TG Stat.

For this, you will use Python packages such as `telethon` to automate the extraction of data from these Telegram channels. The process may involve creating custom scripts or simply exporting data directly from the Telegram application.

#### Image Scraping for Object Detection

Along with text data, images from selected Telegram channels will be scraped for object detection. The relevant Telegram channels include:

- Chemed Telegram Channel
- Yetenaweg

The images will be processed later for object detection.

#### Storing Raw Data

The raw data collected during scraping will first be stored in a temporary storage location, such as a local database or files, before being processed further.

#### Monitoring and Logging

Implement logging to track the progress of the scraping process. This should capture any errors, failures, or issues during data extraction. Proper monitoring ensures that the process runs smoothly and any issues are easily identified and fixed.

---

### Task 2: Data Cleaning and Transformation

#### Data Cleaning

Once the data is scraped, the next step is cleaning the data. This includes:

- **Removing Duplicates**: Ensure that the data contains no repeated or redundant entries.
- **Handling Missing Values**: Missing values need to be addressed by either filling them with suitable values or removing rows with missing values.
- **Standardizing Formats**: Ensure that all data follows a consistent format for easier processing and analysis.
- **Data Validation**: Validate the data to ensure its correctness and consistency before storing it in the database.

#### Storing Cleaned Data

Once cleaned, the data will be stored in a permanent database. The cleaned data should be indexed and partitioned properly to ensure efficient querying and retrieval.

#### DBT for Data Transformation

For transforming the data into its final form suitable for analysis, you will use DBT (Data Build Tool). This involves the following steps:

1. **Install and Set Up DBT**: Install DBT using:

    ```bash
    pip install dbt
    dbt init my_project
    ```

2. **Define DBT Models**: DBT models are SQL files that define the transformations on your data.

3. **Run the DBT Models**: The models will transform and load the data into your data warehouse.

    ```bash
    dbt run
    ```

4. **Perform Data Quality Checks**: Use DBT’s testing and documentation features to ensure the data meets quality standards.

    ```bash
    dbt test
    dbt docs generate
    dbt docs serve
    ```

---

### Task 3: Object Detection Using YOLO

#### Setting Up the Environment

For object detection, YOLO (You Only Look Once) will be used. You will need to install the necessary dependencies, such as OpenCV, TensorFlow, or PyTorch, depending on the YOLO version being used.

- Install Required Libraries:

    ```bash
    pip install opencv-python
    pip install torch torchvision  # For PyTorch-based YOLO
    pip install tensorflow  # For TensorFlow-based YOLO
    ```

#### Download YOLO Model

Clone the YOLO repository from GitHub and install its dependencies:

```bash
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
To expose the collected data via an API, you will use FastAPI and Uvicorn. First, install the required packages:

pip install fastapi uvicorn

Create FastAPI Application

Set up the following project structure for your FastAPI application:

my_project/
├── main.py
├── database.py
├── models.py
├── schemas.py
└── crud.py

    main.py will contain the main FastAPI application and API routes.
    database.py will contain the configuration for the database connection using SQLAlchemy.
    models.py will define SQLAlchemy models for the database tables.
    schemas.py will define Pydantic schemas for data validation and serialization.
    crud.py will contain CRUD (Create, Read, Update, Delete) operations for the database.

Running the API Server

Finally, to run the FastAPI application, use the following command:

uvicorn main:app --reload

This will expose the collected data via API endpoints, allowing access to the data for analysis or reporting.

# Conclusion

This project will provide a scalable and efficient solution for scraping, cleaning, and transforming data related to Ethiopian medical businesses. The integration of YOLO-based object detection will enhance the data collection process, and FastAPI will provide easy access to the data via APIs. The result will be a robust data warehouse that can store and process large amounts of data, enabling actionable insights for decision-makers.
Dependencies

    telethon for Telegram scraping
    opencv-python, torch, tensorflow for YOLO-based object detection
    dbt for data transformation
    fastapi and uvicorn for building and exposing the API