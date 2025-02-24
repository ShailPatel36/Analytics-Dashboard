# Analytics Dashboard

This project is a web-based analytics dashboard built using FastAPI and Plotly. It provides interactive visualizations for user analytics, merchandising strategy, and targeting strategy.

## Features

- **User Analytics Dashboard**: Visualizes session duration distribution and trends over time.
- **Merchandising Strategy Dashboard**: Displays store metrics relationships and factor importance in sales.
- **Targeting Strategy Dashboard**: Shows customer segmentation and factor importance in customer value.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/analytics-dashboard.git
   cd analytics-dashboard
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the FastAPI server**:
   ```bash
   uvicorn main:app --reload
   ```

2. **Open your browser** and go to `http://127.0.0.1:8000/` to view the dashboard.

## Dependencies

- FastAPI
- Uvicorn
- Pandas
- NumPy
- Scikit-learn
- Plotly

## Project Structure

- `main.py`: The main application file containing all endpoints and logic.
- `requirements.txt`: A list of Python packages required to run the application.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
