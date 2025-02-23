from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse, FileResponse
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine

app = FastAPI()

# Create an in-memory SQLite database (or use a file-based DB)
DATABASE_URL = "sqlite:///./data.db"
engine = create_engine(DATABASE_URL)


@app.get("/", response_class=HTMLResponse)
def read_root():
    # Generate data for each dashboard
    user_data = generate_mock_data()
    avg_session_time = user_data["session_duration"].mean()
    drop_off_rate = user_data["drop_off_rate"].mean()
    user_fig1 = px.histogram(
        user_data, x="session_duration", title="Distribution of Session Duration")
    user_fig2 = px.scatter(user_data, x="user_id", y="session_duration",
                           title="Session Duration Trend Over Time")

    store_data = pd.DataFrame({
        "store_id": range(1, 101),
        "traffic": np.random.randint(1000, 10000, 100),
        "conversion_rate": np.random.uniform(0.05, 0.3, 100),
        "assortment_quality": np.random.uniform(1, 5, 100)
    })
    store_fig1 = px.scatter_matrix(store_data, dimensions=["traffic", "conversion_rate", "assortment_quality"],
                                   title="Store Metrics Relationships")
    store_fig2 = go.Figure(data=[go.Bar(
        x=['Traffic', 'Conversion Rate', 'Assortment Quality'],
        y=LinearRegression().fit(store_data[["traffic", "conversion_rate", "assortment_quality"]],
                                 store_data["traffic"] * store_data["conversion_rate"]).coef_,
        name='Factor Importance'
    )])
    store_fig2.update_layout(title="Factor Importance in Sales")

    customer_data = pd.DataFrame({
        "customer_id": range(1, 5001),
        "income_level": np.random.randint(30000, 150000, 5000),
        "spend_per_visit": np.random.uniform(50, 500, 5000),
        "visit_frequency": np.random.poisson(5, 5000),
    })
    customer_fig1 = px.scatter(customer_data, x="income_level", y="spend_per_visit",
                               size="visit_frequency", title="Customer Segmentation")
    customer_fig2 = go.Figure(data=[go.Bar(
        x=['Income Level', 'Spend per Visit', 'Visit Frequency'],
        y=LinearRegression().fit(customer_data[["income_level", "spend_per_visit", "visit_frequency"]],
                                 customer_data["spend_per_visit"] * customer_data["visit_frequency"]).coef_,
        name='Factor Importance'
    )])
    customer_fig2.update_layout(title="Factor Importance in Customer Value")

    # Combine all content into one HTML page
    html_content = f"""
    <html>
        <head>
            <title>Analytics Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }}
                .section {{ margin-bottom: 40px; }}
                .metric {{ padding: 10px; margin: 10px 0; background-color: #f0f0f0; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <h1>Welcome to Analytics Dashboard</h1>
            <div class="section">
                <h2>User Analytics Dashboard</h2>
                <div class="metric">Average Session Time: {avg_session_time:.2f} seconds</div>
                <div class="metric">Drop-off Rate: {drop_off_rate:.2%}</div>
                <div>{user_fig1.to_html(full_html=False)}</div>
                <div>{user_fig2.to_html(full_html=False)}</div>
            </div>
            <div class="section">
                <h2>Merchandising Strategy Dashboard</h2>
                <div>{store_fig1.to_html(full_html=False)}</div>
                <div>{store_fig2.to_html(full_html=False)}</div>
            </div>
            <div class="section">
                <h2>Targeting Strategy Dashboard</h2>
                <div>{customer_fig1.to_html(full_html=False)}</div>
                <div>{customer_fig2.to_html(full_html=False)}</div>
            </div>
        </body>
    </html>
    """
    return html_content


def generate_mock_data():
    return pd.DataFrame({
        "user_id": range(1, 1001),
        "session_duration": np.random.normal(60, 20, 1000),
        "drop_off_rate": np.random.uniform(0, 1, 1000)
    })


@app.get("/analyze", response_class=HTMLResponse)
def analyze_user_data():
    data = generate_mock_data()

    # Calculate engagement metrics
    avg_session_time = data["session_duration"].mean()
    drop_off_rate = data["drop_off_rate"].mean()

    # Create visualizations
    fig1 = px.histogram(data, x="session_duration",
                        title="Distribution of Session Duration")
    fig2 = px.scatter(data, x="user_id", y="session_duration",
                      title="Session Duration Trend Over Time")

    # Predict future engagement using Linear Regression
    data["user_index"] = np.arange(len(data))
    model = LinearRegression()
    model.fit(data[["user_index"]], data["session_duration"])
    future_engagement = model.predict([[len(data) + 1]])[0]

    html_content = f"""
    <html>
        <head>
            <title>User Analytics Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .metric {{ 
                    padding: 10px; 
                    margin: 10px 0; 
                    background-color: #f0f0f0; 
                    border-radius: 5px; 
                }}
                .back-link {{
                    margin-bottom: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="back-link">
                <a href="/">← Back to Home</a>
            </div>
            <h1>User Analytics Dashboard</h1>
            <div class="metric">Average Session Time: {avg_session_time:.2f} seconds</div>
            <div class="metric">Drop-off Rate: {drop_off_rate:.2%}</div>
            <div class="metric">Predicted Future Engagement: {future_engagement:.2f} seconds</div>
            <div>{fig1.to_html(full_html=False)}</div>
            <div>{fig2.to_html(full_html=False)}</div>
        </body>
    </html>
    """
    return html_content


@app.get("/merchandising-strategy", response_class=HTMLResponse)
def merchandising_strategy():
    # Mock store data
    store_data = pd.DataFrame({
        "store_id": range(1, 101),
        "traffic": np.random.randint(1000, 10000, 100),
        "conversion_rate": np.random.uniform(0.05, 0.3, 100),
        "assortment_quality": np.random.uniform(1, 5, 100)
    })

    # Regression model to find key factors affecting sales
    X = store_data[["traffic", "conversion_rate", "assortment_quality"]]
    y = store_data["traffic"] * store_data["conversion_rate"]
    model = LinearRegression()
    model.fit(X, y)
    importance = model.coef_

    # Create visualizations
    fig1 = px.scatter_matrix(store_data, dimensions=["traffic", "conversion_rate", "assortment_quality"],
                             title="Store Metrics Relationships")
    fig2 = go.Figure(data=[go.Bar(
        x=['Traffic', 'Conversion Rate', 'Assortment Quality'],
        y=importance,
        name='Factor Importance'
    )])
    fig2.update_layout(title="Factor Importance in Sales")

    html_content = f"""
    <html>
        <head>
            <title>Merchandising Strategy Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .back-link {{
                    margin-bottom: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="back-link">
                <a href="/">← Back to Home</a>
            </div>
            <h1>Merchandising Strategy Dashboard</h1>
            <div>{fig1.to_html(full_html=False)}</div>
            <div>{fig2.to_html(full_html=False)}</div>
        </body>
    </html>
    """
    return html_content


@app.get("/targeting-strategy", response_class=HTMLResponse)
def targeting_strategy():
    # Mock fashion company customer data
    customer_data = pd.DataFrame({
        "customer_id": range(1, 5001),
        "income_level": np.random.randint(30000, 150000, 5000),
        "spend_per_visit": np.random.uniform(50, 500, 5000),
        "visit_frequency": np.random.poisson(5, 5000),
    })

    # Identifying key segmentation factors
    X = customer_data[["income_level", "spend_per_visit", "visit_frequency"]]
    y = customer_data["spend_per_visit"] * customer_data["visit_frequency"]
    model = LinearRegression()
    model.fit(X, y)
    importance = model.coef_

    # Create visualizations
    fig1 = px.scatter(customer_data, x="income_level", y="spend_per_visit",
                      size="visit_frequency", title="Customer Segmentation")
    fig2 = go.Figure(data=[go.Bar(
        x=['Income Level', 'Spend per Visit', 'Visit Frequency'],
        y=importance,
        name='Factor Importance'
    )])
    fig2.update_layout(title="Factor Importance in Customer Value")

    html_content = f"""
    <html>
        <head>
            <title>Targeting Strategy Dashboard</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .back-link {{
                    margin-bottom: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="back-link">
                <a href="/">← Back to Home</a>
            </div>
            <h1>Targeting Strategy Dashboard</h1>
            <div>{fig1.to_html(full_html=False)}</div>
            <div>{fig2.to_html(full_html=False)}</div>
        </body>
    </html>
    """
    return html_content


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
