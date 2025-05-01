# REST API Service - Cafe API

## 📌 Overview
This project demonstrates how to build a REST API from scratch using Flask. 
The API provides endpoints to interact with data on cafes that are suitable for remote work. 
You can fetch a random cafe, search for cafes by location, add new cafes, and update cafe details.

このプロジェクトは、Flaskを使用してゼロからREST APIを構築する方法を示しています。
このAPIは、リモートワークに適したカフェのデータを操作するためのエンドポイントを提供します。
ランダムなカフェを取得したり、ロケーションでカフェを検索したり、新しいカフェを追加したり、カフェの詳細を更新したりすることができます。

## 📌 API Endpoints

### HTTP GET - Random Cafe
Endpoint: `/random`  
Description: Fetches a random cafe from the database.  
Example Request: `http://127.0.0.1:5000/random`    
Response:
```json
{
    "cafe": [
        {
            "can_take_calls": false,
            "coffee_price": "£3.00",
            "has_sockets": true,
            "has_toilet": true,
            "has_wifi": true,
            "id": 7,
            "img_url": "https://lh3.googleusercontent.com/p/AF1QipP_NbZH7A1fIQyp5pRm1jOGwzKsDWewaxka6vDt=s0",
            "location": "Shoreditch",
            "map_url": "https://g.page/acehotellondon?share",
            "name": "Ace Hotel Shoreditch",
            "seats": "50+"
        }
    ]
}
```

### HTTP GET - All Cafes
Endpoint: `/all`  
Description: Fetches all cafes from the database.  
Example Request: `http://127.0.0.1:5000/all`  
Response:  
```json
{
    "cafe": [
        {
            "can_take_calls": false,
            "coffee_price": "£3.00",
            "has_sockets": true,
            "has_toilet": true,
            "has_wifi": true,
            "id": 7,
            "img_url": "https://lh3.googleusercontent.com/p/AF1QipP_NbZH7A1fIQyp5pRm1jOGwzKsDWewaxka6vDt=s0",
            "location": "Shoreditch",
            "map_url": "https://g.page/acehotellondon?share",
            "name": "Ace Hotel Shoreditch",
            "seats": "50+"
        },
        {
            "can_take_calls": true,
            "coffee_price": "£3.00",
            "has_sockets": false,
            "has_toilet": true,
            "has_wifi": true,
            "id": 14,
            "img_url": "https://images.adsttc.com/media/images/5014/ec99/28ba/0d58/2800/0d0f/large_jpg/stringio.jpg?1414576924",
            "location": "Barbican",
            "map_url": "https://goo.gl/maps/XPrcFj91LsQBvUa27",
            "name": "Barbican Centre",
            "seats": "50+"
        }
    ]
}
```

### HTTP GET - Search for a Cafe
Endpoint: `/search?loc=<location>`  
Description: Searches for cafes in a specific location.  
Example Request:  `http://127.0.0.1:5000/search?loc=Barbican`  
Response:  
```json
{
    "cafe": [
        {
            "can_take_calls": true,
            "coffee_price": "£3.00",
            "has_sockets": false,
            "has_toilet": true,
            "has_wifi": true,
            "id": 14,
            "img_url": "https://images.adsttc.com/media/images/5014/ec99/28ba/0d58/2800/0d0f/large_jpg/stringio.jpg?1414576924",
            "location": "Barbican",
            "map_url": "https://goo.gl/maps/XPrcFj91LsQBvUa27",
            "name": "Barbican Centre",
            "seats": "50+"
        }
    ]
}
```

## 📌 API Usage Example with Postman

### Get Random Cafe

Send a GET request to `http://localhost:5000/random`.  
This will return a random cafe from the database.

### Get All Cafes

Send a GET request to `http://localhost:5000/all`.  
This will return a list of all cafes in the database.   

### Search Cafes by Location

Send a GET request to `http://localhost:5000/search?loc=Tokyo`.  
This will search for cafes in the specified location (Tokyo in this case).   

### Add a New Cafe (HTTP POST)

Send a POST request with cafe details (e.g., name, location, price) to `http://localhost:5000/add`.  
This will add a new cafe to the database.

### Update a Cafe's Coffee Price (HTTP PATCH)

Send a PATCH request to `http://localhost:5000/update-price/<cafe_id>` with the new coffee price.  
This will update the coffee price for the specified cafe.

### Delete a Cafe (HTTP DELETE)

Send a DELETE request to `http://localhost:5000/report-closed/<cafe_id>` with an API key.  
This will mark the specified cafe as closed and remove it from the database.

## 📌 Documentation

You can find the complete [API Documentation](https://documenter.getpostman.com/view/44595462/2sB2j4eqm2) published on Postman.   

[APIドキュメント](https://documenter.getpostman.com/view/44595462/2sB2j4eqm2)はPostmanで公開されています。  
