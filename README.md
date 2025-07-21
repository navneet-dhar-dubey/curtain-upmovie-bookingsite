

# CurtainUp - Movie Booking Website

A full-stack web application built with Django that allows users to browse movies, select seats from an interactive map, and book tickets online. This project demonstrates a complete end-to-end booking flow, including user authentication and payment gateway integration.

**Live Demo:** `[Link to your Vercel URL]`

-----

## ✨ Features

  * **Movie Listings:** Browse a grid of currently showing movies.
  * **Dynamic Filtering & Search:** Filter movies by city and search by title in real-time.
  * **Detailed Movie Pages:** View movie descriptions, ratings, languages, and showtimes grouped by theater and date.
  * **User Authentication:** Secure user registration, login, and logout functionality.
  * **Interactive Seat Selection:** A visual, grid-based seat map that shows available, booked, and selected seats.
  * **Booking System:** A complete booking process that saves user selections to the database.
  * **Payment Gateway Integration:** Secure payment processing using the Razorpay API with webhook verification for payment confirmation.
  * **User Dashboard:** A "My Bookings" page for users to view their booking history.
  * **Custom Admin Command:** A Django management command to automatically generate seats for a new theater screen, simplifying site administration.

-----

## 🛠️ Tech Stack

  * **Backend:** Python, Django
  * **Frontend:** HTML, CSS, JavaScript
  * **Database:** SQLite3 (for development)
  * **Payment Gateway:** Razorpay API
  * **Deployment:** Vercel

-----

## 🚀 Getting Started

To run this project locally, follow these steps:

1.  Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  Create and activate a virtual environment:

    ```bash
    python -m venv venv
    use `venv\Scripts\activate`
    ```

3.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4.  Apply database migrations:

    ```bash
    python manage.py migrate
    ```

5.  Run the development server:

    ```bash
    python manage.py runserver
    ```
