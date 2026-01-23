
const fs = require('fs');
const path = require('path');

const GPM_PATH = path.join(__dirname, '../data/pressure-matrix.json');
const MOCK_DATA = {
    "store": "Alpha Medical",
    "version": "1.0.0",
    "last_updated": new Date().toISOString(),
    "overall_pressure": 42,
    "sectors": {
        "operations": {
            "shopify": {
                "pressure": 30, // Healthy
                "trend": "STABLE",
                "last_check": new Date().toISOString(),
                "sensor_data": {
                    "products_total": 78,
                    "products_active": 78,
                    "orders_today": 12, // Simulated
                    "orders_unfulfilled": 2
                }
            }
        },
        "marketing": {
            "klaviyo": {
                "pressure": 25, // Healthy
                "trend": "DOWN",
                "last_check": new Date().toISOString(),
                "sensor_data": {
                    "lists_total": 5,
                    "flows_active": 3,
                    "campaigns_last_30d": 2
                }
            },
            "ga4": {
                "pressure": 60,
                "sensor_data": {
                    "roas": "2.4",
                    "revenue_7d": "1500.00"
                }
            }
        },
        "retention": {
            "churn": {
                "pressure": 15,
                "sensor_data": {
                    "churnRate": "2.1%"
                }
            }
        }
    }
};

fs.writeFileSync(GPM_PATH, JSON.stringify(MOCK_DATA, null, 2));
console.log('✅ GPM Stimulated with Mock Data for System Verification');
