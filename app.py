from flask import Flask, render_template, jsonify
import pandas as pd
import json

app = Flask(__name__, template_folder='.')

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
    # 1. ДИНАМИКА ПРОДАЖ ПО ДНЯМ
    sales['sale_date'] = pd.to_datetime(sales['transaction_date']).dt.date
    sales_by_day = sales.groupby('sale_date')['quantity'].sum()
    sales_by_day = {str(date): value for date, value in sales_by_day.items()}
    
    # 2. ДИНАМИКА СОБЫТИЙ ПО ДНЯМ
    events['event_date'] = pd.to_datetime(events['event_timestamp']).dt.date
    events_by_day = events.groupby('event_date').size()
    events_by_day = {str(date): value for date, value in events_by_day.items()}
    
    # 3. ВОРОНКА СОБЫТИЙ
    events_funnel = events.groupby('event_type').size().to_dict()
    
    # 4. ПРОДАЖИ ПО КАТЕГОРИЯМ
    sales_with_categories = pd.merge(sales, products, on='product_id')
    sales_by_category = sales_with_categories.groupby('category')['quantity'].sum().to_dict()
    
    # 5. СЕГМЕНТАЦИЯ КЛИЕНТОВ
    customers_by_segment = user_segments.groupby('segment').size().to_dict()
    
    # 6. ВОЗВРАТЫ
    returns_analysis = returns.groupby('reason').size().to_dict()
    returns_with_categories = pd.merge(returns, products, on='product_id')
    returns_category = returns_with_categories.groupby('category').size().to_dict()
    
    # 7. ОСНОВНЫЕ МЕТРИКИ
    total_sales = sales['quantity'].sum()
    total_returns = len(returns)
    total_events = len(events)
    total_customers = len(user_segments)

    # РАСЧЕТ ЧИСТОЙ ВЫРУЧКИ
    planned_revenue = sales['amount'].sum() if 'amount' in sales.columns else 0
    returns_amount = returns['refund_amount'].sum() if 'refund_amount' in returns.columns else 0
    net_revenue = planned_revenue - returns_amount

    # ОБРАЩЕНИЕ В ПОДДЕРЖКУ
    metrics_for_support = customer_support.groupby('issue_type').size().to_dict()
    resolved_issues = customer_support.groupby('resolved').size().to_dict() if 'resolved' in customer_support.columns else {}
    
    # КАНАЛЫ ТРАФИКА
    canal_of_traffic = traffic.groupby('channel').size().to_dict()
    device_of_traffic = traffic.groupby('device').size().to_dict()
    
    # ОСТАТКИ НА СКЛАДЕ
    inventory_ = pd.merge(inventory, products, on='product_id')
    
    # Используем правильную колонку для количества
    inventory_qty_col = 'stock_quantity' if 'stock_quantity' in inventory_.columns else 'quantity'
    inventory_by_category = inventory_.groupby('category')[inventory_qty_col].sum().to_dict()

    # Используем правильную колонку для даты обновления
    inventory_date_col = 'last_updated' if 'last_updated' in inventory_.columns else 'last_update'
    if inventory_date_col in inventory_.columns:
        inventory_last_update = inventory_.groupby(inventory_date_col)[inventory_qty_col].sum()
        inventory_last_update = {str(date): value for date, value in inventory_last_update.items()}
    else:
        inventory_last_update = {}
    
    # РЕКЛАМА
    ad_revenue_ = pd.merge(ad_revenue, products, on='product_id')

    # Траты по датам (преобразуем даты в строки)
    if 'date' in ad_revenue.columns and 'spend' in ad_revenue.columns:
        ad_spend_data = ad_revenue.groupby('date')['spend'].sum()
        ad_spend = {str(date): value for date, value in ad_spend_data.items()}
    else:
        ad_spend = {}

    # Количество рекламных кампаний по категориям
    ad_category = ad_revenue_.groupby('category').size().to_dict()

    # Впечатления по категориям
    ad_impressions = ad_revenue_.groupby('category')['impressions'].sum().to_dict() if 'impressions' in ad_revenue_.columns else {}
    
    # ДОХОДЫ ПОСТАВЩИКОВ
    suppliers_revenue = pd.merge(sales, products, on='product_id')
    suppliers_revenue = pd.merge(suppliers_revenue, suppliers, on='supplier_id')
    
    # Используем правильную колонку для дохода
    revenue_col = 'amount' if 'amount' in suppliers_revenue.columns else 'rating'
    revenue_by_supplier = suppliers_revenue.groupby('supplier_name')[revenue_col].sum().to_dict()
    
    return render_template(
        'index.html',
        # Данные для графиков
        sales_by_day=json.dumps(sales_by_day),
        events_by_day=json.dumps(events_by_day),
        events_funnel=json.dumps(events_funnel),
        sales_by_category=json.dumps(sales_by_category),
        customers_by_segment=json.dumps(customers_by_segment),
        returns_analysis=json.dumps(returns_analysis),
        returns_category=json.dumps(returns_category),
        net_revenue=net_revenue,  # Убрал json.dumps - это число!
        metrics_for_support=json.dumps(metrics_for_support),
        resolved_issues=json.dumps(resolved_issues),
        canal_of_traffic=json.dumps(canal_of_traffic),
        device_of_traffic=json.dumps(device_of_traffic),
        inventory_by_category=json.dumps(inventory_by_category),
        inventory_last_update=json.dumps(inventory_last_update),
        ad_spend=json.dumps(ad_spend),
        ad_category=json.dumps(ad_category),
        ad_impressions=json.dumps(ad_impressions),
        revenue_by_supplier=json.dumps(revenue_by_supplier),
        
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
