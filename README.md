# Reggio Hub Challenge - IREN - Data Valorization for Waste Management

## Iren Group Challenge: Overview

### Company Profile

**Iren Group** is a leading multi-utility company in Italy, operating across diverse sectors including electricity, gas, district heating, integrated water management, environmental services, and technological solutions. The Group employs over **8,600 people**, serves **1.9 million energy customers**, manages water services for **2.8 million inhabitants**, and provides environmental services for **3.1 million inhabitants**. Organized into four business units—Networks, Environment, Energy, and Market—Iren is a trusted partner for public administrations and communities, focusing on sustainable growth and leveraging innovation to meet customer and citizen needs.

### Challenge

The challenge seeks **innovative and sustainable solutions** to improve **waste management** and **plant monitoring** for **Iren Ambiente**. Participants are tasked with processing data collected from vehicles and waste treatment facilities using advanced technologies, such as **neural networks** and **mathematical modeling**, to derive new insights or optimize resources. Proposed solutions should aim to enhance operational performance, reduce environmental impact, or uncover unavailable information. Where applicable, solutions should include modeling, simulation, and data visualization tools to assess performance and illustrate findings.

Read more on the [Reggio Hub Challenge website](https://reggiohub.it/talent-roadshow/)

## Our Proposed Solution

![logo](media/logo.png)

We proposed a smart monitoring system that employs cameras on waste management vehicles.
Using Computer Vision algorithms with Artificial Intelligence, the cameras can identify, classify and track the position and type of abandoned waste in the streets, sending real-time data to the operational center of IREN.
The data con be aggregated with the already existing one of IREN (like the bins positions and vehicle optimized routes) to then employ data analysis and extract business intelligence information to:

- identify critical waste areas
- plan new bins installations
- predict with AI algorithm waste position, type
- track waste automatically for the new upcoming ARERA standards
- track bins condition
- identify anomalies and bottlenecks

Read our [presentation/pitch deck](https://www.canva.com/design/DAGXSwYaIjk/SCSYonaK8hrFkJICOxKFaA/view?utm_content=DAGXSwYaIjk&utm_campaign=designshare&utm_medium=link&utm_source=editor)

## Demo

Our demo simulates, with artificial data, a dashboard to visualize waste on a city map (Turin in our example).
The waste can be filtered and visualized by types with color coding and also by what information channel was used to detect it.
Then, the filtered data can be employed to predict with a Machine Learning model, the future days positions and types of waste.

### Map

![dashboard example](media/dashboard_map.png)

## Predictions of waste position and type

![dashboard preds](media/dashboard_predictions.png)


## Our Team

![team](media/team.png)

Contacts (LinkedIn):
- [Cristina Vercellino]()
- [Jamila Mansour]()
- [Ettore Candeloro]()

## Installation of the demo app

Install poetry globally with python (version 3.10 or more), then use the following commands:

    poetry config settings.virtualenvs.in-project true
    
    poetry install

Then run the project with:

    poetry shell

    python main.py

The server with be launched at localhost (http://127.0.0.1:8050/), so you can visualize it with a browser.

If all is good you will see:

    Dash is running on http://127.0.0.1:8050/
    *Serving Flask app 'main'
    *Debug mode: on
 

