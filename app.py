from flask import Flask, render_template, jsonify
import pandas as pd
import json

app = Flask(__name__)

# Загрузка данных
ad_revenue = pd.read_csv('tablats/ad_revenue.csv')
customer_support = pd.read_csv('tablats/customer_support.csv')
events = pd.read_csv('tablats/events.csv')
inventory = pd.read_csv('tablats/inventory.csv')
products = pd.read_csv('tablats/products.csv')
returns = pd.read_csv('tablats/returns.csv')
sales = pd.read_csv('tablats/sales.csv')
suppliers = pd.read_csv('tablats/suppliers.csv')
traffic = pd.read_csv('tablats/traffic.csv')
user_segments = pd.read_csv('tablats/user_segments.csv')

@app.route('/')
def dashboard():
    # 1. ДИНАМИКА ПРОДАЖ ПО ДНЯМ (из sales - transaction_date)
    sales['sale_date'] = pd.to_datetime(sales['transaction_date']).dt.date
    sales_by_day = sales.groupby('sale_date')['quantity'].sum().to_dict()
    
    # 2. ДИНАМИКА СОБЫТИЙ ПО ДНЯМ (из events)
    events['event_date'] = pd.to_datetime(events['event_timestamp']).dt.date
    events_by_day = events.groupby('event_date').size().to_dict()
    
    
    # 3. ВОРОНКА СОБЫТИЙ (показы → клики → корзина → покупки)
    events_funnel = events.groupby('event_type').size().to_dict()
    
    # 4. ПРОДАЖИ ПО КАТЕГОРИЯМ (объединяем sales и products)
    sales_with_categories = pd.merge(sales, products, on='product_id')
    sales_by_category = sales_with_categories.groupby('category')['quantity'].sum().to_dict()
    
    # 5. СЕГМЕНТАЦИЯ КЛИЕНТОВ (из user_profiles)
    customers_by_segment = user_segments.groupby('segment').size().to_dict()
    
    # 6. ВОЗВРАТЫ (анализ из returns)
    returns_analysis = returns.groupby('return_reason').size().to_dict()
    retturns_with_categories = pd.merge(returns, products, on='product_id')
    returns_category = retturns_with_categories.groupby('category').size().to_dict()
    # 7. ОСНОВНЫЕ МЕТРИКИ
    total_sales = sales['quantity'].sum()
    total_returns = len(returns)
    total_events = len(events)
    total_customers = len(user_segments)
    
    #обращение в поддержку
    metrics_for_support_b =customer_support.groupby('issue_type').size()
    metrics_for_support=metrics_for_support_b.to_dict()
    resolved_issues =metrics_for_support_b.groupby('resolved').size().to_dict()

    return render_template(
        'index.html',
        # Данные для графиков
        sales_by_day=json.dumps(sales_by_day),
        events_by_day=json.dumps(events_by_day),
        events_funnel=json.dumps(events_funnel),
        sales_by_category=json.dumps(sales_by_category),
        customers_by_segment=json.dumps(customers_by_segment),
        returns_analysis=json.dumps(returns_analysis),
        
        # Основные метрики
        total_sales=total_sales,
        total_returns=total_returns,
        total_events=total_events,
        total_customers=total_customers
    )

@app.route('/api/sales')
def api_sales():
    return jsonify(sales.to_dict(orient='records'))

@app.route('/api/events')
def api_events():
    return jsonify(events.to_dict(orient='records'))

if __name__ == '__main__':
    
    app.run(debug=True)
