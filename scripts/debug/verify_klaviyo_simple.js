
require('dotenv').config({ path: '.env.admin' });
const axios = require('axios');

const API_KEY = 'pk_6579ec83387884b95a0ff47d0b70ebbae9'; // Testing the key found in KLAVIYO_PUBLIC_API_KEY

if (!API_KEY) {
    console.error('❌ No API Key found in .env.admin or environment.');
    process.exit(1);
}

console.log(`🔑 Using Key matching prefix: ${API_KEY.substring(0, 7)}...`);

async function checkKlaviyo() {
    try {
        console.log('📡 Testing connection to https://a.klaviyo.com/api/lists/');
        const response = await axios.get('https://a.klaviyo.com/api/lists/', {
            headers: {
                'Authorization': `Klaviyo-API-Key ${API_KEY}`,
                'revision': '2024-02-15'
            }
        });
        console.log('✅ Success! Status:', response.status);
        console.log('📦 Data received:', JSON.stringify(response.data.data ? response.data.data.length : response.data, null, 2));
    } catch (error) {
        console.error('❌ Error:', error.response ? error.response.status : error.message);
        if (error.response) {
            console.error('Response data:', JSON.stringify(error.response.data, null, 2));
        }
    }
}

checkKlaviyo();
