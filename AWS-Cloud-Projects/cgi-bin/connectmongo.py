import pymongo
import json

def lambda_handler(event, context):
    # MongoDB connection details (replace with your actual details)
    mongo_uri = "mongodb://username:password@your-mongodb-host:27017/your-database"
    
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(mongo_uri)
        db = client['your-database']
        collection = db['your-collection']

        # Perform a simple query (example)
        data = collection.find_one({"key": "value"})

        # Close the MongoDB connection
        client.close()

        # Prepare response
        return {
            'statusCode': 200,
            'body': json.dumps(data, default=str)  # Convert BSON to JSON-friendly format
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


