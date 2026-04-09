# AQI Monitor — Real-time Air Quality Monitoring System

## Overview
An automated Python pipeline that fetches real-time Air Quality Index (AQI) 
and pollutant data for 4 Indian cities, flags anomalies, and visualizes 
trends through a Tableau dashboard.

## Cities Tracked
- Delhi
- Mumbai
- Bengaluru
- Pilani

## Features
- Real-time AQI and pollutant data fetching via OpenWeatherMap API
- Automated hourly data collection using Python scheduler
- Threshold-based anomaly detection (AQI >= 3 flagged as Alert)
- Structured CSV logging with timestamps for trend analysis
- Tableau dashboard with AQI trends, city comparisons and PM2.5 analysis

## Tech Stack
- Python 3.14.3
- Libraries: requests, pandas, schedule
- Tableau Desktop
- OpenWeatherMap API

## How to Run
1. Clone the repository
2. Install dependencies: pip install requests pandas schedule
3. Add your OpenWeatherMap API key in fetch_aqi.py
4. Run: python fetch_aqi.py
5. Script will fetch data every hour automatically

## Dashboard
The Tableau dashboard includes:
- AQI by City — bar chart comparing current AQI levels
- AQI Trend Over Time — line chart showing AQI changes hourly
- PM2.5 by City — pollutant comparison across cities
