1.Install python 3.

2. Open terminal in project root folder. 

2. run command: pip install -r requirements.txt

3. Run server: python main.py

API:

127.0.0.1:5000/api/config - returns config from json file
127.0.0.1:5000/static/images/gears.jpg - returns image
127.0.0.1:5000/api/country?id=ua - request for json by country ID 
    allowed IDs: uk, us, ua, de