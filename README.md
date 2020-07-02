<h1 align="center">
COD Tournament Backend
</h1>
Built with Flask. API URL: 

## 🚀 Quick start

1.  **Install**

    Navigate into the site’s directory and start it up.

    ```shell
    cd cat-app-backend/
    
    python3 -m venv env
    
    .\env\Scripts\activate
    
    pip3 install -r requirements.txt
    ```
    
1. **Configure credentials.py**
    ```
    MYSQL_USER='YOUR_DB_USERNAME'
    MYSQL_PASSWORD='YOUR_DB_PASSWORD'
    MYSQL_HOST='YOUR_DB_HOST'
    MYSQL_DB='YOUR_DB_NAME'
    SECRET_KEY='YOUR_SECRET_KEY'
    ```

1. **Configure .flaskenv**
    ```
    FLASK_APP=app
    FLASK_ENV=development
    ```
   
1.  **Initialize DB**
    ```
    flask db init
    flask db migrate
    flask db upgrade
    ```
    
1.  **Demo Data**
    ```
    flask create_demo_data
    flask delete_demo_data
    ```
   
   
1.  **Run script**
    ```shell
    flask run
    ```


1.  **Start Celery Worker**
    ```
    celery worker -A celery_worker.celery --loglevel=info --pool=solo
    ```
   
   
1.  **Monitor Celery**
    ```
    celery -A celery_worker.celery flower
    ```


