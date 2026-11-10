import json
import os
import uuid
import boto3
import datetime 
from html import escape

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def response(status, message):
    return {
        "statusCode":status,
        "headers":{"Content-Type": "application/json"},
        "body":json.dumps(message)
        }

def put_task(taskId, title):
    task = {
            "taskId":taskId,
            "title": title
           }

    table.put_item(Item=task)
    return response(201, {"message": "Task saved","task":task})

def get_task(task_id):
    result = table.get_item(Key = {"taskId": task_id})
    task = result.get("Item")
    if task is None:
        return response(404, {"message": "Task not found"})
    return task_page(task)

def show_task(task):
    task_id = escape(str(task["taskId"]))
    title = escape(str(task["title"]))

    html = f"""
    <html>
    <head>
        <meta name="viewport"
              content="width=device-width, initial-scale=1">
        <title>My Task App</title>
    </head>
    <body style="font-family: Arial; padding: 20px;">
        <h2>My First AWS Task App</h2>
        <p>This is my first project using AWS Lambda and DynamoDB.</p>
        <hr>

        <p><b>Task ID:</b> {task_id}</p>
        <p><b>Title:</b> {title}</p>

        <p style="color: green;">Task loaded successfully!</p>
    </body>
    </html>
    """

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html; charset=utf-8"},
        "body": html
    }



def lambda_handler(event, context):

    # method = event.get("httpMethod")
    method = event["requestContext"]["http"]["method"]

    if method == "GET":
        # task_id = event.get("taskId")
        task_id = event["pathParameters"]["taskId"]
        return get_task(task_id)
    
    elif method == "PUT":
        body = json.loads(event["body"])
        task_id = body.get("taskId")
        title = body.get("title")
        print("Saving task:", task_id)
        return put_task(task_id, title)

    return response(405, {
        "message": "Method not allowed"
    })
        


def task_page(task):
    title = escape(str(task.get("title", "Untitled")))
    task_id = escape(str(task.get("taskId", "")))

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport"
              content="width=device-width, initial-scale=1">
        <title>My Task App</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #eef2f7;
                padding: 24px;
            }}
            .card {{
                background: white;
                padding: 28px;
                border-radius: 16px;
                max-width: 420px;
                margin: 50px auto;
                box-shadow: 0 5px 20px #ddd;
            }}
            h1 {{ color: #222; }}
            .tag {{
                color: #087443;
                background: #dff8e9;
                padding: 8px 12px;
                border-radius: 8px;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>My Task App</h2>
            <p>Powered by AWS Lambda + DynamoDB</p>
            <hr>
            <h1>{title}</h1>
            <p>Task ID: {task_id}</p>
            <span class="tag">Loaded from DynamoDB</span>
        </div>
    </body>
    </html>
    """

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html; charset=utf-8"},
        "body": html
    }


    
    


    


