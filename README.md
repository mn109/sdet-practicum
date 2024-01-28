# Selenium Automation Testing Project

## Introduction

This project contains automated tests for a website using Selenium WebDriver with Python. The tests follow the Page Object Model (POM) design pattern, which makes test maintenance easier.

## Prerequisites

Before running the tests, ensure you have the following installed:
- Python 3.10
- Chrome browser
- ChromeDriver compatible with your Chrome version

## Installation

- Clone the repository. Yes, you will need some ridiculous stuff like the AI-generated .jpeg picture of the non-existing person allegedly filling the form with his fake personal data and the .crx file of an ad-blocking Chrome plugin (uBlock Origin, in case you are interested) helping the man along by killing nasty Google ads.
- Set up a virtual environment.
- Install the requirements: `pip install -r requirements.txt`

## Running the tests
Run the tests: `pytest test.py`.  
Should the `ElementClickInterceptedException` occur, run the tests again: the adblock occasionally fails to clear the way.