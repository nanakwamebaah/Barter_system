# Barter Platform

A Django-based monolithic web application that allows users to post ads for goods they want to exchange, browse other users' ads, and send exchange proposals.

## Features

* User signup, login, and logout
* Create, edit, delete ads
* Search and filter ads by keywords, category, and condition
* Create, view, and update exchange proposals
* Detail pages for ads and proposals

## Technology Stack

* Python 3.8+
* Django 4.x
* SQLite (default) or PostgreSQL
* Bootstrap 5 for styling

## Prerequisites

* Python 3.8 or higher
* Git

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/nanakwamebaah/Barter_system.git
   cd barter_platform
   ```

2. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```



## Database Migrations

Run the following commands to apply migrations and prepare the database:

```bash
python manage.py makemigrations
python manage.py migrate
```




## Running the Development Server

Start the local server:

```bash
python manage.py runserver
```

Open your browser and go to `http://127.0.0.1:8000/`.

## Running Tests

All tests are located in the `ads/tests.py` file. To run them:

```bash
python manage.py test ads
```

You should see output indicating the number of tests run and their status.

## Usage

1. **Sign Up / Login**: Create a new account or log in.
2. **Post New Ad**: Click "Post New Ad" in the navbar to create an ad.
3. **Browse Ads**: On the home page, search or filter ads.
4. **Ad Detail**: Click an ad title to view details and propose an exchange.
5. **Manage Proposals**: View, accept or reject proposals under "Proposals".


---


