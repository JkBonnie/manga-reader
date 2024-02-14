# Manga Recap with GPT-4 Vision

## Project Overview

This project aims to generate summaries of manga chapters by analyzing images extracted from PDF files of the manga. It utilizes the GPT-4 Vision API to understand the content of manga pages and produce compelling, story-telling tone summaries. The project processes PDFs to extract images, scales them to a specific size, encodes them in base64, and then uses these images as input for the GPT-4 Vision API alongside custom prompts to generate summaries.

## Features

- PDF processing to extract manga pages as images.
- Image scaling to fit the requirements of the GPT-4 Vision API.
- Base64 encoding of images for API submission.
- Customizable prompts for generating summaries in a story-telling tone.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- Pip (Python package manager)
- Virtual environment (recommended)

## Installation Steps

1. Create a virtual environment to manage your project's dependencies separately.

```
python3 -m venv venv
```
2. Activate the virtual environment

```
source venv/bin/activate
```

3. Install Required Python Packages

```
pip3 install -r requirements.txt
```

4. Set Up Environment Variables

```
OPENAI_API_KEY=your_openai_api_key_here
```

5. Prepare Your Manga PDFs

Place your manga PDF files in a directory structure as expected by the script, for example, `naruto-v10/` containing chapters as PDF files.


## Running the Project

To run the project, execute the `app.py` script from the root directory of your project:
```
python3 app.py
```

This script processes the specified PDF files, extracts and scales images, encodes them in base64, and sends them to the GPT-4 Vision API for analysis. The summaries generated by the API are printed to the console, including the total tokens used.







