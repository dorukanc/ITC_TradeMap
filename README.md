Here's an updated version of your `README.md` file with all comments translated into English and a note about this being a fork from Ponggung.

```markdown
# ITC_TradeMap

This project is a fork of the original project by Ponggung.

1. Web Scraping
2. HTML Parsing
3. Converting Data to JSON Format
4. Deploying the API on GCP App Engine

## Main Program

| Step | Work Description                   | Code       |
|------|------------------------------------|------------|
| 1    | Web Scraping                       | spider.py  |
| 2    | HTML Parsing                       | parser.py  |
| 3    | Convert DataFrame Format to JSON   | toJson.py  |

## Web Scraping

- **Target Website**: [ITC Trade Map](https://www.trademap.org/Country_SelProduct_TS.aspx)
- **Website Description**: ITC Trade Map database contains import and export records of agricultural products from various countries around the world.
- **Scraping Requirements**: Download monthly import and export values and volumes for specific items.

1. Use Python Selenium package  
2. Login is required to select the items needed for the task

### Specific Settings for Scraping:

1. **Products**:
   - "020711 - Fresh or chilled fowls of the species Gallus domesticus, not cut in pieces"
   - "020712 - Frozen fowls of the species Gallus domesticus, not cut in pieces"
   - "020714 - Frozen cuts and edible offal of fowls of the species Gallus domesticus"
   - "040700 - Birds' eggs, in shell, fresh, preserved or cooked"

2. **Countries**: "World"

3. **Records**: ["Exports", "Imports"]

4. **Time Series**: "Monthly time series"

5. **Indicators**: ["Values", "Quantities"]

6. **Time Period (number of columns)**: "20 per page"

7. **Rows per page**: "300 per page"

8. All other settings use default website values.

![web](img/web.png)  
![df](img/df.png)

## Installation

```bash
sudo pip install -r requirement.txt
```

## Web Driver

- **Firefox 64.0**, **Geckodriver v0.23.0**  
  You need to install the driver and Firefox version corresponding to your OS. In this example, the macOS version is installed. The version of Geckodriver must match the Firefox version and Selenium version. Usually, the latest versions work well together.

```bash
wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-macos.tar.gz
tar -zxvf geckodriver-v0.23.0-macos.tar.gz
```

- **PhantomJS 2.1.1**  
  Use Anaconda to install PhantomJS:

```bash
conda install -y -c conda-forge phantomjs
```

## Docker

```bash
docker build -t itc_trade_spider:latest -f Dockerfile .
docker run itc_trade_spider
```

## Quick Test

```bash
python spider.py
python parser.py
python toJson.py
check.ipynb
```

## Run the Program

```bash
python run.py
```

![log](img/log.png)

## Output

The program will generate the following output files:

```
df_all.pickle
map_result.json
```

![json](img/json.png)
```

This `README.md` file provides an overview of the project, instructions for installation and setup, and details on how to run and test the code. It also includes comments translated into English for better understanding.