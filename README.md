# Wind Analysis and Wind Rose Animation – Iguape, Brazil

Python tools for wind data analysis and animated wind rose visualization using meteorological observations from Iguape, São Paulo, Brazil.

## Overview

This repository contains two applications:

### 1. Wind Climatology Analysis

Generates:

* Wind statistics
* Wind rose
* Daily mean wind speed
* Monthly mean wind speed
* Diurnal wind cycle
* Wind speed distribution histogram

### 2. Animated Wind Rose

Creates a daily animated wind rose sequence and exports it as an MP4 video using FFmpeg.

The animation is designed for scientific communication, presentations, social media, and LinkedIn posts.

---

## Example Output

### Wind Analysis

* Wind Rose
* Daily Mean Wind Speed
* Monthly Mean Wind Speed
* Diurnal Cycle
* Wind Speed Histogram

### Animation

Daily evolution of wind conditions including:

* Wind speed distribution
* Prevailing wind direction
* Mean wind speed
* Maximum gust
* Timeline progress bar

Output:

```text
windrose_iguape_linkedin.mp4
```

---

## Data Format

The scripts expect CSV files exported from the meteorological station containing at least the following columns:

```text
Data
Hora (UTC)
Vel. Vento (m/s)
Dir. Vento (m/s)
Raj. Vento (m/s)
```

Example:

```text
01/10/2024 ; 1200 ; 2.3 ; 145 ; 4.7
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/wind-analysis-iguape.git

cd wind-analysis-iguape
```

Create a virtual environment:

```bash
python3 -m venv windetec

source windetec/bin/activate
```

Install dependencies:

```bash
pip install pandas matplotlib windrose numpy
```

---

## FFmpeg Installation

The animation script requires FFmpeg.

Ubuntu / Debian:

```bash
sudo apt install ffmpeg
```

Verify installation:

```bash
ffmpeg -version
```

---


## Running the Wind Analysis

```bash
python3 iguapewind.py
```

Generated plots:

* Wind Rose
* Daily Mean Wind Speed
* Monthly Mean Wind Speed
* Diurnal Wind Cycle
* Wind Speed Distribution

---

## Running the Animation

Edit the desired time interval:

```python
INICIO = '2024-10-01'
FIM = '2024-12-01'
```

Run:

```bash
python3 windrose_linkedin.py
```

The script will:

1. Read all CSV files
2. Generate one frame per day
3. Save PNG frames
4. Build an MP4 animation using FFmpeg

Output:

```text
windrose_iguape_linkedin.mp4
```

---

## Animation Features

Each frame displays:

* Wind rose
* Daily mean wind speed
* Daily maximum gust
* Cardinal wind direction
* Timeline progress bar
* Scientific visualization footer

---

## Scientific Applications

This project can be used for:

* Boundary Layer Meteorology
* Wind Climatology
* Atmospheric Monitoring
* Environmental Studies
* Renewable Energy Assessment
* Scientific Outreach

---

## Requirements

* Python ≥ 3.10
* Pandas
* Matplotlib
* Windrose
* NumPy
* FFmpeg

---

## Author

Mateus Fernandes Rodrigues

Remote Sensing and Atmospheric Boundary Layer Research

University of São Paulo (USP)

---

