"""
Author: Joe Cranney
Project Title: Virtual Card Generator
Project Description: Generates payment cards from Privacy and Stripe
Date Created: 6/1/2020
Last Edited: 6/1/2020
"""

import sys
import json
import stripe
from packages import generator
from datetime import datetime

if __name__ == "__main__":
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - VIRTUAL CARD GENERATOR")
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Created by @atcbackdoor")

    try:
        generator.validate_files()
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - {e}")
        sys.exit()

    config = json.load(open("config.json"))
    stripe.api_key = config["stripe"]

    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - [1] Create Stripe Card Holder")
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - [2] Create Stripe Cards")
    print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - [3] Create Privacy Cards")
    selection = str(input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Select an option to continue: "))

    if selection == "1":
        full_name = input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Enter full name: ")
        email = input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Enter email: ")
        telephone = input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Enter phone number: ")
        address1 = input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Enter address 1: ")
        address2 = input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Enter address 2: ")
        city = input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Enter city: ")
        state = input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Enter state: ")
        country = input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Enter country: ")
        postal_code = input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Enter postal code: ")

        address = {
            "line1": address1,
            "city": city,
            "state": state,
            "country": country,
            "postal_code": postal_code
        }

        if address2 is not "":
            address["line2"] = address2

        cardholder = generator.create_stripe_cardholder(full_name, email, telephone, address)

        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Created cardholder with ID: {cardholder['id']}")

    elif selection == "2":
        cardholder = input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Enter cardholder id: ")
        quantity = input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Enter quantity: ")

        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - WARNING: STRIPE CHARGES $0.10 PER CARD")
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - You will be charged ${float(quantity) * 0.10}")
        input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Press any key to continue: ")
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Generating cards...")

        cards = []

        for _ in range(int(quantity)):
            card = generator.create_stripe_card(cardholder)
            cards.append(card)

        generator.write_stripe_cards_to_file(cards)
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Success! Cards exported to cards.xls in main folder")

    elif selection == "3":
        quantity = input(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Enter quantity: ")
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Generating cards...")
        for _ in range(int(quantity)):
            generator.create_privacy_card(config["privacy"])

        print(f"[{datetime.now().strftime('%H:%M:%S.%f')}] - Success! Note, privacy forces you to get cards via "
              f"dashboard")
