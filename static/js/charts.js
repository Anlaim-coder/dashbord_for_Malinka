// charts.js
document.addEventListener('DOMContentLoaded', function() {
    // Ждем полной загрузки данных
    setTimeout(initCharts, 100);
});

function initCharts() {
    // 1. ГРАФИК ПРОДАЖ ПО ДНЯМ (линейный)
    if (window.salesByDay && Object.keys(window.salesByDay).length > 0) {
        const salesCtx = document.getElementById('salesChart').getContext('2d');
        const dates = Object.keys(window.salesByDay);
        const salesData = Object.values(window.salesByDay);
        
        new Chart(salesCtx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: 'Продажи по дням',
                    data: salesData,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Динамика продаж по дням'
                    }
                }
            }
        });
    }

    // 2. ПРОДАЖИ ПО КАТЕГОРИЯМ (столбчатая)
    if (window.salesByCategory && Object.keys(window.salesByCategory).length > 0) {
        const categoryCtx = document.getElementById('categoryChart').getContext('2d');
        const categories = Object.keys(window.salesByCategory);
        const salesByCat = Object.values(window.salesByCategory);
        
        new Chart(categoryCtx, {
            type: 'bar',
            data: {
                labels: categories,
                datasets: [{
                    label: 'Продажи по категориям',
                    data: salesByCat,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Продажи по категориям товаров'
                    }
                }
            }
        });
    }

    // 3. ОСТАТКИ НА СКЛАДЕ (pie chart)
    if (window.inventoryByCategory && Object.keys(window.inventoryByCategory).length > 0) {
        const inventoryCtx = document.getElementById('inventoryChart').getContext('2d');
        const inventoryCategories = Object.keys(window.inventoryByCategory);
        const inventoryData = Object.values(window.inventoryByCategory);
        
        new Chart(inventoryCtx, {
            type: 'pie',
            data: {
                labels: inventoryCategories,
                datasets: [{
                    data: inventoryData,
                    backgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56',
                        '#4BC0C0',
                        '#9966FF',
                        '#FF9F40'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Остатки товаров по категориям'
                    },
                    legend: {
                        position: 'right'
                    }
                }
            }
        });
    }

    // 4. ВОЗВРАТЫ (bar chart)
    if (window.returnsAnalysis && Object.keys(window.returnsAnalysis).length > 0) {
        const returnsCtx = document.getElementById('returnsChart').getContext('2d');
        const reasons = Object.keys(window.returnsAnalysis);
        const returnsData = Object.values(window.returnsAnalysis);
        
        new Chart(returnsCtx, {
            type: 'bar',
            data: {
                labels: reasons,
                datasets: [{
                    label: 'Количество возвратов',
                    data: returnsData,
                    backgroundColor: 'rgba(255, 99, 132, 0.7)'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Анализ возвратов по причинам'
                    }
                }
            }
        });
    }

    // 5. РАСХОДЫ НА РЕКЛАМУ (line chart)
    if (window.adSpend && Object.keys(window.adSpend).length > 0) {
        const adSpendCtx = document.getElementById('adSpendChart').getContext('2d');
        const adDates = Object.keys(window.adSpend);
        const spendData = Object.values(window.adSpend);
        
        new Chart(adSpendCtx, {
            type: 'line',
            data: {
                labels: adDates,
                datasets: [{
                    label: 'Расходы на рекламу',
                    data: spendData,
                    borderColor: 'rgb(255, 159, 64)',
                    backgroundColor: 'rgba(255, 159, 64, 0.2)',
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Динамика расходов на рекламу'
                    }
                }
            }
        });
    }

    // 6. ЭФФЕКТИВНОСТЬ РЕКЛАМЫ (bar chart)
    if (window.adImpressions && Object.keys(window.adImpressions).length > 0) {
        const adImpCtx = document.getElementById('adImpressionsChart').getContext('2d');
        const adCategories = Object.keys(window.adImpressions);
        const impressionsData = Object.values(window.adImpressions);
        
        new Chart(adImpCtx, {
            type: 'bar',
            data: {
                labels: adCategories,
                datasets: [{
                    label: 'Количество показов',
                    data: impressionsData,
                    backgroundColor: 'rgba(153, 102, 255, 0.7)'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Эффективность рекламы по категориям'
                    }
                }
            }
        });
    }

    // 7. СЕГМЕНТЫ КЛИЕНТОВ (doughnut)
    if (window.customersBySegment && Object.keys(window.customersBySegment).length > 0) {
        const clientsCtx = document.getElementById('clientsChart').getContext('2d');
        const segments = Object.keys(window.customersBySegment);
        const segmentData = Object.values(window.customersBySegment);
        
        new Chart(clientsCtx, {
            type: 'doughnut',
            data: {
                labels: segments,
                datasets: [{
                    data: segmentData,
                    backgroundColor: [
                        '#FF6384',
                        '#36A2EB',
                        '#FFCE56',
                        '#4BC0C0',
                        '#9966FF'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Сегментация клиентов'
                    },
                    legend: {
                        position: 'right'
                    }
                }
            }
        });
    }

    // 8. ВОРОНКА СОБЫТИЙ (bar chart - вертикальный)
    if (window.eventsFunnel && Object.keys(window.eventsFunnel).length > 0) {
        const funnelCtx = document.getElementById('funnelChart').getContext('2d');
        const eventTypes = Object.keys(window.eventsFunnel);
        const eventData = Object.values(window.eventsFunnel);
        
        new Chart(funnelCtx, {
            type: 'bar',
            data: {
                labels: eventTypes,
                datasets: [{
                    label: 'Количество событий',
                    data: eventData,
                    backgroundColor: 'rgba(54, 162, 235, 0.7)'
                }]
            },
            options: {
                responsive: true,
                indexAxis: 'y', // Горизонтальные столбцы для воронки
                plugins: {
                    title: {
                        display: true,
                        text: 'Воронка событий пользователей'
                    }
                }
            }
        });
    }
}