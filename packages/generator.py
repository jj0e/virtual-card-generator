"""
Author: Joe Cranney
Project Title: Virtual Card Generator
Project Description: Generates payment cards from Privacy and Stripe
Date Created: 6/1/2020
Last Edited: 6/1/2020
"""

import os
import json
import stripe
import requests
from xlwt import Workbook


def validate_files():
    if not os.path.exists("config.json"):
        raise Exception("config.json file is missing.")
    else:
        config = json.load(open("config.json"))
        if config["stripe"] == "":
            raise Exception("Missing stripe api key in config.json")
        if config["privacy"] == "":
            raise Exception("Missing privacy api key in config.json")


def create_stripe_cardholder(full_name, email, telephone, address):
    cardholder = stripe.issuing.Cardholder.create(
        type="individual",
        name=full_name,
        email=email,
        phone_number=telephone,
        billing={
            "address": address
        }
    )

    return cardholder


def create_stripe_card(cardholder_id, currency="usd"):
    card = stripe.issuing.Card.create(
        cardholder=cardholder_id,
        currency=currency,
        type="virtual"
    )

    details = stripe.issuing.Card.details(card["id"])

    return details


def create_privacy_card(api):
    headers = {
        "Authorization": f"api-key {api}"
    }

    response = requests.post("https://api.privacy.com/v1/card", headers=headers, json={"type": "MERCHANT_LOCKED"})

    return response


def write_stripe_cards_to_file(cards):
    workbook = Workbook()
    sheet = workbook.add_sheet("Cards")
    sheet.write(0, 0, "Profile Name")
    sheet.write(0, 1, "First Name")
    sheet.write(0, 2, "Last Name")
    sheet.write(0, 3, "Email")
    sheet.write(0, 4, "Telephone")
    sheet.write(0, 5, "Address 1")
    sheet.write(0, 6, "Address 2")
    sheet.write(0, 7, "City")
    sheet.write(0, 8, "State")
    sheet.write(0, 9, "Country")
    sheet.write(0, 10, "Postal Code")
    sheet.write(0, 11, "Card Number")
    sheet.write(0, 12, "Exp month")
    sheet.write(0, 13, "Exp year")
    sheet.write(0, 14, "CVC")

    for card in cards:
        index = cards.index(card) + 1
        sheet.write(index, 1, card["card"]["cardholder"]["name"].split(" ")[0])
        sheet.write(index, 2, card["card"]["cardholder"]["name"].split(" ")[1])
        sheet.write(index, 3, card["card"]["cardholder"]["email"])
        sheet.write(index, 4, card["card"]["cardholder"]["phone_number"])
        sheet.write(index, 5, card["card"]["cardholder"]["billing"]["address"]["line1"])
        sheet.write(index, 6, card["card"]["cardholder"]["billing"]["address"]["line2"])
        sheet.write(index, 7, card["card"]["cardholder"]["billing"]["address"]["city"])
        sheet.write(index, 8, card["card"]["cardholder"]["billing"]["address"]["state"])
        sheet.write(index, 9, card["card"]["cardholder"]["billing"]["address"]["country"])
        sheet.write(index, 10, card["card"]["cardholder"]["billing"]["address"]["postal_code"])
        sheet.write(index, 11, card["number"])
        sheet.write(index, 12, card["exp_month"])
        sheet.write(index, 13, card["exp_year"])
        sheet.write(index, 14, card["cvc"])

    workbook.save("cards.xls")
