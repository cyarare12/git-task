#!/usr/bin/env python
"""
Test script for Twitter integration functionality.
This script tests the Twitter posting functionality without requiring real API credentials.
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from ecommerce.functions.tweet import Tweet

def test_twitter_integration():
    """Test the Twitter integration functionality"""
    print("Testing Twitter Integration")
    print("=" * 50)

    # Test 1: Create Tweet instance
    print("\n1. Creating Tweet instance...")
    try:
        tweet_instance = Tweet()
        print("SUCCESS: Tweet instance created successfully")
    except Exception as e:
        print(f"FAILED: Failed to create Tweet instance: {e}")
        return

    # Test 2: Test store creation tweet
    print("\n2. Testing store creation tweet...")
    store_tweet = {
        "text": "Exciting news! We've just launched 'TechZone Electronics' - your one-stop shop for all things tech!\n\nVisit us at: http://127.0.0.1:8000/"
    }

    try:
        response = tweet_instance.make_tweet(store_tweet)
        print("SUCCESS: Store creation tweet posted successfully!")
        print(f"Tweet ID: {response.get('data', {}).get('id', 'N/A')}")
    except Exception as e:
        print(f"FAILED: Failed to post store tweet: {e}")

    # Test 3: Test product creation tweet
    print("\n3. Testing product creation tweet...")
    product_tweet = {
        "text": "New arrival! Check out our latest iPhone 15 Pro - now available at TechZone Electronics!\n\nPrice: R25,999\n\nShop now: http://127.0.0.1:8000/"
    }

    try:
        response = tweet_instance.make_tweet(product_tweet)
        print("SUCCESS: Product creation tweet posted successfully!")
        print(f"Tweet ID: {response.get('data', {}).get('id', 'N/A')}")
    except Exception as e:
        print(f"FAILED: Failed to post product tweet: {e}")

    # Test 4: Test multiple tweets
    print("\n4. Testing multiple tweets...")
    tweets = [
        {"text": "Flash Sale! 20% off on all electronics this weekend!"},
        {"text": "Free delivery on orders over R500!"},
        {"text": "Customer favorite: Our gaming laptops are flying off the shelves!"}
    ]

    for i, tweet in enumerate(tweets, 1):
        try:
            response = tweet_instance.make_tweet(tweet)
            print(f"SUCCESS: Tweet {i} posted successfully!")
        except Exception as e:
            print(f"FAILED: Failed to post tweet {i}: {e}")

    print("\n" + "=" * 50)
    print("Twitter integration test completed!")
    print("\nNote: All tweets above were simulated in TEST MODE.")
    print("To use real Twitter API, set TWITTER_TEST_MODE=false and add real API credentials.")

if __name__ == "__main__":
    test_twitter_integration()