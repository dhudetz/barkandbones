This repo runs the barknbones.org website.

Prod environment:
1. frontend/config.js  ->  config value set to PI_BASE_URL: ""
2. nginx server should be running with proxy to /api for port 5001
    note: change default proxy ports at /etc/nginx/sites-enabled
3. run the python backend using <code>python3 backend/app.py</code>

Dev environment:
1. frontend/config.js  ->  config value set to PI_BASE_URL: "http://localhost:5001"
2. start python frontend web server using <code>python3 -m http.server</code>
3. start python backend app using <code>python3 backend/app.py</code>