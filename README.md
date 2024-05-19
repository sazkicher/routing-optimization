# Routing Optimization

This repository contains a solution for the Capacitated Vehicle Routing Problem (CVRP) using an OSRM server and Google OR Tools. The primary functionality is encapsulated in the `RoutingModel.py` script, the code reads the coordinates given in the `subbase.xlx` file which is the set of stops to optimize.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Links](#links)

## Introduction

The Capacitated Vehicle Routing Problem (CVRP) is a classic optimization problem in logistics where the goal is to determine the optimal set of routes for limited number of vehicles and its capacity. This solution leverages:

- **OSRM (Open Source Routing Machine)**: An open-source routing engine designed for use with OpenStreetMap (OSM) data. It provides high-performance routing capabilities.
- **Google OR Tools**: A robust suite of optimization tools developed by Google that includes algorithms for solving routing problems.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.12 installed on your local machine


## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/sazkicher/routing-optimization.git
    cd routing-optimization
    ```

2. **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```


## Usage

To solve the CVRP, you will primarily interact with the `RoutingModel.py` script. Below is a basic example of how to run the script:

```bash
python RoutingModel.py
```

The code reads the coordinates given in the `subbase.xlsx` file, which contains the set of stops to optimize. If you want to calculate routes for different coordinates, you should modify the `subbase.xlsx` file with the new set of stops.

Please note that the code currently has hardcoded values and only accepts three initial points: `cnt`, `txt`, and `mdn`. These can be changed if needed by updating the corresponding sections in the script `matrixRoutes.py`.


## Links

- **OSRM (Open Source Routing Machine)**:
  - [OSRM GitHub Repository](https://github.com/Project-OSRM/osrm-backend)
  - [OSRM API Documentation](http://project-osrm.org/docs/v5.24.0/api/#general-options)

- **Google OR Tools**:
  - [Google OR Tools GitHub Repository](https://github.com/google/or-tools)
  - [Google OR Tools Documentation](https://developers.google.com/optimization)