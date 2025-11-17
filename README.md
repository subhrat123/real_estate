# Real Estate AI Analyst

This project is a web application that provides real estate analysis using a generative AI model. It features a chatbot interface where users can ask questions about real estate trends in natural language.

## Features

-   **Chatbot Interface**: Ask questions about real estate in plain English.
-   **Single Location Analysis**: Get a detailed analysis for a single location, including price trends, demand insights, and investment attractiveness.
-   **Multi-Location Comparison**: Compare multiple locations to see which one is a better investment.
-   **Rich Visualizations**: The analysis is presented with a summary, a chart, and a table.

## Technology Stack

### Backend

-   [Django](https://www.djangoproject.com/)
-   [Django Rest Framework](https://www.django-rest-framework.org/)
-   [Google Generative AI (Gemini)](https://ai.google.dev/)
-   [Pandas](https://pandas.pydata.org/)

### Frontend

-   [React](https://reactjs.org/)
-   [Vite](https://vitejs.dev/)
-   [Axios](https://axios-http.com/)
-   [Recharts](https://recharts.org/)
-   [Tailwind CSS](https://tailwindcss.com/)

## Getting Started

### Prerequisites

-   Python 3.10+
-   Node.js 14+
-   A Google AI API key.

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd Real_estate_project/backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your environment variables:**
    Create a `.env` file in the `Real_estate_project/backend` directory and add your Google AI API key:
    ```
    GOOGLE_API_KEY=your_api_key
    ```

5.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The backend will be running at `http://127.0.0.1:8000`.

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd Real_estate_project/frontend
    ```

2.  **Install the dependencies:**
    ```bash
    npm install
    ```

3.  **Run the development server:**
    ```bash
    npm run dev
    ```
    The frontend will be running at `http://localhost:5173` (or another port if 5173 is busy).

## Usage

Once both the backend and frontend servers are running, open your browser and go to the frontend URL. You will see a chat interface where you can ask questions about real estate.

**Examples:**

-   `What is the price trend in Thane?`
-   `Compare Thane vs Vashi`
-   `Can you analyze Bandra, Andheri, and Dadar?`

## API Endpoint

The application uses a single API endpoint for all chat interactions:

-   **URL:** `/api/chat/`
-   **Method:** `POST`
-   **Body:**
    ```json
    {
        "query": "your natural language query"
    }
    ```
