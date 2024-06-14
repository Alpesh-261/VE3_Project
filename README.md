# CSV Analysis Django Project

## Setup Instructions

1. Install dependencies:
    ```bash
    pip install django pandas numpy matplotlib seaborn base64
    ```

2.Create project and startapp
    ```bash
    django-admin startproject csv_analysis
    python manage.py startapp analysis
    ```

3.Create models,forms,views and urls in analysis app
    ```models.py
       forms.py
       views.py
       urls.py
    ```


4. Create and apply migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Run the development server:
    ```bash
    python manage.py runserver
    ```

6. Open your browser and navigate to:
    ```
    http://127.0.0.1:8000/
    ```

7. Upload a CSV file to see the data analysis and visualizations.

## Brief explanation of the project

This Django project allows users to upload CSV files for analysis. The analysis includes displaying the first few rows of the data, calculating summary statistics, identifying missing values, and generating histograms for numerical columns. The results and visualizations are displayed on the web interface.
