import json
import os
from datetime import datetime

# Check if we're in test mode (no real Twitter credentials)
TEST_MODE = os.getenv('TWITTER_TEST_MODE', 'true').lower() == 'true'

if not TEST_MODE:
    from requests_oauthlib import OAuth1Session
    # Twitter API credentials (you need to get these from Twitter Developer Portal)
    CONSUMER_KEY = 'your_consumer_key_here'
    CONSUMER_SECRET = 'your_consumer_secret_here'
else:
    # Mock credentials for testing
    CONSUMER_KEY = 'test_key'
    CONSUMER_SECRET = 'test_secret'

class Tweet:
    _instance = None
    oauth = None

    def __new__(cls):
        if cls._instance is None:
            print('Creating the Tweet object')
            cls._instance = super(Tweet, cls).__new__(cls)
            cls._instance.authenticate()
        return cls._instance

    def authenticate(self):
        if TEST_MODE:
            print("Twitter integration running in TEST MODE - no real authentication required")
            self.oauth = "test_oauth_session"
            return

        # Real Twitter authentication
        request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
        oauth = OAuth1Session(CONSUMER_KEY, client_secret=CONSUMER_SECRET)

        try:
            fetch_response = oauth.fetch_request_token(request_token_url)
        except ValueError:
            print("There may have been an issue with the consumer_key or consumer_secret you entered.")
            return

        resource_owner_key = fetch_response.get("oauth_token")
        resource_owner_secret = fetch_response.get("oauth_token_secret")
        print("Got OAuth token: %s" % resource_owner_key)

        # Get authorization
        base_authorization_url = "https://api.twitter.com/oauth/authorize"
        authorization_url = oauth.authorization_url(base_authorization_url)
        print("Please go here and authorize: %s" % authorization_url)
        verifier = input("Paste the PIN here: ")

        # Get the access token
        access_token_url = "https://api.twitter.com/oauth/access_token"
        oauth = OAuth1Session(
            CONSUMER_KEY,
            client_secret=CONSUMER_SECRET,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=verifier,
        )
        oauth_tokens = oauth.fetch_access_token(access_token_url)

        access_token = oauth_tokens["oauth_token"]
        access_token_secret = oauth_tokens["oauth_token_secret"]

        # Make the request
        self.oauth = OAuth1Session(
            CONSUMER_KEY,
            client_secret=CONSUMER_SECRET,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )

    def make_tweet(self, tweet):
        if TEST_MODE:
            # Test mode - simulate successful tweet
            print("TEST MODE: Simulating Twitter post...")
            print(f"Tweet content: {tweet.get('text', 'No text')}")
            print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # Simulate successful response
            mock_response = {
                "data": {
                    "id": f"test_tweet_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "text": tweet.get('text', ''),
                    "created_at": datetime.now().isoformat(),
                    "author_id": "test_user_123"
                },
                "meta": {
                    "test_mode": True,
                    "message": "Tweet simulated successfully (no real Twitter API call)"
                }
            }

            print("TEST TWEET SUCCESSFUL!")
            print(json.dumps(mock_response, indent=4, sort_keys=True))
            return mock_response

        # Real Twitter API mode
        if self.oauth:
            # Making the request
            response = self.oauth.post(
                "https://api.twitter.com/2/tweets",
                json=tweet,
            )
        else:
            raise ValueError('Authentication failed!')

        if response.status_code != 201:
            raise Exception(
                "Request returned an error: {} {}".format(response.status_code, response.text)
            )

        print("Response code: {}".format(response.status_code))

        # Saving the response as JSON
        json_response = response.json()
        print(json.dumps(json_response, indent=4, sort_keys=True))
        return json_response