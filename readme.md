This repo runs the barknbones.org website.

Prod environment:
1. frontend/config.js  ->  config value set to API_BASE_URL: "http://barknbones.org"
2. nginx server should be running with proxy to /api for port 5001
    note: change default proxy ports at /etc/nginx/sites-available/default
3. python backend should be running in a docker container

Dev environment:
1. frontend/config.js  ->  config value set to API_BASE_URL: "http://localhost:5001"
2. start python frontend web server through docker-compose in /frontend
3. start python backend app using <code>python3 backend/app.py</code>