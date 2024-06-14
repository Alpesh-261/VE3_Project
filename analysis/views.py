import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
import base64
from io import BytesIO
from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm

def handle_uploaded_file(file):
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    elif file.name.endswith('.xlsx'):
        df = pd.read_excel(file)
    else:
        raise ValueError("Unsupported file format")
    
    required_columns = ['Duration', 'Pulse', 'Maxpulse', 'Calories']
    
    for column in required_columns:
        if column not in df.columns:
            raise KeyError(f"Required column '{column}' is missing in the uploaded file")
    
    # print("DataFrame Info:")
    # print(df.info())
    
    summary = df[required_columns].copy()
    return summary

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                file = request.FILES['file']
                summary = handle_uploaded_file(file)
                analysis_result = analyze_data(summary)
                context = {
                    'form': form,
                    'analysis_result': analysis_result,
                }
                return render(request, 'analysis/results.html', context)
            except (ValueError, KeyError) as e:
                return HttpResponse(f"Error: {e}", status=400)
        else:
            return HttpResponse("Invalid form submission", status=400)
    else:
        form = UploadFileForm()
    return render(request, 'analysis/upload.html', {'form': form})

def analyze_data(data):
    analysis_result = {}
    analysis_result['head'] = data.head().to_html()

    # Calculating summary statistics
    summary_stats = data.agg(['mean', 'median', 'std']).T
    summary_stats_html = summary_stats.to_html()
    analysis_result['summary_stats'] = summary_stats_html

    # Handling missing values
    missing_values = data.isnull().sum().reset_index()
    missing_values.columns = ['Column', 'Missing Values']
    analysis_result['missing_values'] = missing_values.to_html(index=False)

    # Generate plots
    plots = generate_plots(data)
    analysis_result.update(plots)

    return analysis_result

def generate_plots(data):
    plots = {}
    numerical_columns = data.select_dtypes(include=[np.number]).columns.tolist()

    for column in numerical_columns:
        plt.figure()
        sns.histplot(data[column].dropna(), kde=True)
        plt.title(f'Histogram of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')

        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
        buf.close()
        plt.close()

        plots[f'{column}_histogram'] = f'data:image/png;base64,{image_base64}'

    return plots
