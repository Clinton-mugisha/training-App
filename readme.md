# AI-Driven CV Ranking System .

Welcome to the AI-Driven CV Ranking System. This project is designed to revolutionize the recruitment process by incorporating artificial intelligence to assist recruiters in efficiently assessing and ranking CVs of job applicants.

## Table of Contents

- Features
- Getting Started
  - Prerequisites
  - Installation
- Usage
  - Job Listing
  - Job Details
  - Create Job
  - Create Applicant
- AI CV Ranking
  - Ranking Criteria
  - Machine Learning Model
- Contributing
- License
- Acknowledgments

## Features

- Job Listing: View a comprehensive list of available job positions.
- Job Details: Access detailed information about each job to make informed decisions.
- Create Job: Streamline the process of adding new job listings.
- Create Applicant: Efficiently input and manage applicant information.
- AI CV Ranking: Leverage an advanced AI system to analyze and rank CVs based on predefined criteria.

## Getting Started

## Prerequisites

Before you begin, ensure you have the following prerequisites installed on your system:

- Python: This project requires Python to be installed. You can download and install Python from the official Python website. Make sure to use a version compatible with the project (specified in the requirements.txt file).

- Django: The project uses the Django web framework. Install Django using the following command:

  bash
  pip install Django==5
Additional Dependencies: Install other project dependencies specified in the requirements.txt file. Navigate to the project directory and run:

bash
Copy code
pip install -r requirements.txt

# Installation
Clone the project repository:

bash
Copy code
git clone https://github.com/Clinton-mugisha/training-App
cd training-App
Set up a virtual environment (optional but recommended):

Create a virtual environment to isolate the project dependencies. Run the following commands:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
Install dependencies:

# Install project dependencies within the virtual environment:

bash
Copy code
pip install -r requirements.txt
Set up environment variables:

Create a .env file in the project root and configure any necessary environment variables. For example:

env
Copy code
DEBUG=True
DATABASE_URL=mysql


# Run migrations:

Apply database migrations to set up the database:

bash
Copy code
python manage.py migrate
Create a superuser 

# Create an admin superuser to access the Django admin interface:

bash
Copy code
python manage.py createsuperuser
Follow the prompts to set up the superuser credentials.

# Run the application:

# Start the development server:

bash
Copy code
python manage.py runserver
The application should be accessible at http://localhost:8000/.

# Usage
# Job Listing
Visit http://localhost:8000/jobs/ to explore the list of available job positions.
Job Details
Click on a specific job title to access detailed information about that job.
Create Job
Access http://localhost:8000/create-job/ to effortlessly add new job listings.
Create Applicant
Access http://localhost:8000/create-applicant/ to input and manage detailed applicant information.

        AI CV Ranking
# Ranking Criteria
The AI-driven CV ranking system evaluates CVs based on predefined criteria, including but not limited to:

Educational qualifications
Relevant work experience
Skills and certifications
Machine Learning Model
The system employs a sophisticated machine learning model to analyze CVs and assign ranks. The model continuously learns from data, providing recruiters with accurate and insightful rankings.

# Contributing
We welcome contributions from the community. If you encounter any issues or have suggestions for improvements, please submit a GitHub issue or create a pull request.

# License
This project is licensed under the __ License - see the LICENSE.md file for details.

# Acknowledgments
Special thanks to the Refactory technical team for their continuous support and collaboration on this groundbreaking AI-driven CV ranking project.
