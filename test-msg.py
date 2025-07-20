import os
import requests
import json
import dotenv
dotenv.load_dotenv()

def test_slack_webhook():
    webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    # Try different payload formats
    payload = {
        "text": "Hello from test script",
        "username": "Audit Bot",
        "icon_emoji": ":bell:"
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    try:
        print(f"Sending test message to Slack...")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        # Try with verify=False if SSL is an issue
        response = requests.post(
            webhook_url,
            data=json.dumps(payload),  # Use data instead of json
            headers=headers,
            timeout=10,
            verify=True  # Set to False if SSL issues
        )
        
        print(f"Request URL: {webhook_url}")
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            print("✅ Message sent successfully!")
        else:
            print(f"❌ Failed to send message: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            
    except requests.exceptions.SSLError as e:
        print(f"❌ SSL Error - Try setting verify=False: {str(e)}")
    except Exception as e:
        print(f"❌ Error: {type(e).__name__} - {str(e)}")

if __name__ == "__main__":
    test_slack_webhook()
