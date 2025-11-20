# MBTA-Web-App-Project

This is the base repository for Web App project. Please read the [instructions](instructions.md) for details.

MBTA WEB APP Project - Part 1: Introduction and Problem Definition

### Part 1
1. introduction : This project aims to build a simple MBTA Web App using Python, Flask, and external APIS. The goals is to allow the user to enter a place name or adress and receive the newaster MBTA station possible. This shows how web APIS, backened logis and HTML templates all can create a more dynamic type of web application. 

2. problem defintion: People that travel tend to struggle to identify in a quick manner the nearest MBTA station. The navigation tools can become too brod or hide some important and specigic MBTA information. The problem: How can be create a simple tool that takes a location adn returns the closest MBTA station?

3. Requirements : 
The app must : accept user input, use an external API, contain a python helper file, use Flaks to handle GET/POST request, Render HTML result pages, handle errors 

4. Methods and tools: Python, Flaks, Requests (send API calls), External API (geocoding location), MBTA API (station data) HTML template (output)

5. High level system flow : User enters location → Flask route → mbta_helper.py API call 
→ Find nearest station → return result → display in HTML

