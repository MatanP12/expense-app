
# Expense app

This is a simple expense tracking application implented with Python and Flask using MongoDB Database.




## Tech Stack

**Client:** HTML, JS, CSS

**Server:** Python, Flask

**Database:** MongoDB


## Run Locally

Clone the project

```bash
  git clone git@github.com:MatanP12/expense-app.git
```

Go to the project directory

```bash
  cd expense-app
```

Install dependencies

```bash
  pip Install -r requirments.txt
```

Start the server

```bash
  python src/app.py
```
Or use docker to run the application


```bash
  docker-compose up
```


## API Reference

#### Get all expenses

```http
  GET /expenses
```

#### Create new expense

```http
  POST /expenses
```
##### Request Body:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `product`      | `string` | **Required**. The product's name |
| `price`      | `float` | **Required**. the product's price |



#### Get expense

```http
  GET /expenses/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of expense to fetch |


#### Update expense

```http
  PUT /expenses/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of expense to update |

##### Request Body:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `product`      | `string` | **Required**. The product's name |
| `price`      | `float` | **Required**. the product's price |



#### Delete expense

```http
  DELETE /expenses/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. Id of expense to delete |


## 3 Teir application

![3-Tier application Drawing](https://github.com/MatanP12/expense-app/blob/main/Documents/Expense-app-Application.png?raw=true)

## CI- Pipeline

![CI-Pipeline Drawing](https://raw.githubusercontent.com/MatanP12/expense-app/main/Documents/Expense-app-%20CI.png)

