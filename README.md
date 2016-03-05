# pyBomQuote

This tool helps you to search the pages de.farnell.com and de.rs-online.com for the parts listet in your bill of materials. It collects data like ordercode, price, availability and URL for each product. This information helps you to select the supplier for each product. At the end you can export cart tables which can be uploaded directly to the supplier pages to be added to your shopping cart.

![Mainwindow Screenshot](docs/mainwindow.png?raw=true "Mainwindow Screenshot")

##How to install pBomQuote
You need python2.7 and PySide. PySide can be installed on Windows with
```
 pip install -U PySide 
```
Or
```
 easy_install -U PySide. 
```
the easy_install script is located in the python installation. There might be a problem with the library pyqt. In that case you have to rename the files qt.conf to eg. qt_.conf.

##First start
It is necessary to get a key for the Farnell REST API. Register at [https://partner.element14.com/member/register](https://partner.element14.com/member/register) and get the REST Key. Copy and rename the file pyBomQuote/src/farnell_api/api_config.py to pyBomQuote/src/farnell_api/api_config_my.py.

farnell_api/api_config.py:
```
API_KEY = 'xxxxxxx'
API_STORE = 'de.farnell.com'
```
Replace the xxxxxxx with your REST API Key you just got from the Farnell page and save the file.

##How to use pBomQuote
Start the program with start.py.

pyBomQuote accepts *.csv tables with the pipe symbol '|' as separator with the following format:

| Number | quantity | quantity | Reference | Manufacturer Part Number | Manufacturer | LibRef | Footprint | Description

where Number and Libref are ignored.

An example BOM file looks like:

```
7|1|C8|T491B476K010A|Kemet|T491B476K010A|CAP_POL_3528_TANTALB_HIGHDENS|47u/10V/Tanatal Package B
6|1|C9|GRM188R61H105KAALD|Murata|GRM188R61H105KAALD|cap_0603_highdens|CAP CER 0603 1u 50V X5R 10%
5|3|C12, C18, C21|C1005X5R0J475M050BC|TDK|C1005X5R0J475M050BC|cap_0402_highdens|CAP CER 0402 4u7 6V3 X5R 20%
```

To import that file click on "BOM/quote BOM into quote file". The tool searches now the supplier pages for the parts in the BOM and collects information about them. This process takes some time since RS and Farnell might be quite slow. Therefore the information is stored in the file path/to/BOMFile/Bomfile.BomQuote and can be opened with a click on Quote/Open quote file. Now the entries of the Bom file are displayed together with the information provided by the suppliers. If one entry is colored red, this part couldn’t be found on the supplier's page. If it is colored green the Manufacturer Part Number of the BOM matches with Manufacturer Part Number of the supplier. The checkboxes of the BOM entries are for marking the entry to be correct. The checkboxes of the supplier entries are for selecting which entry will be exported into the shopping cart. With a double click on the supplier entry the browser is opened the supplier page of the product.

Clicking on export carts generates a table for RS and Farnell to be imported directly in the shopping carts.
For Farnell navigate to 
[http://de.farnell.com/webapp/wcs/stores/servlet/QuickOrderView?isQuickPaste=true&catalogId=15001&langId=-3&storeId=10161](http://de.farnell.com/webapp/wcs/stores/servlet/QuickOrderView?isQuickPaste=true&catalogId=15001&langId=-3&storeId=10161)

For RS:
[http://de.rs-online.com/web/ca/Warenkorb/](http://de.rs-online.com/web/ca/Warenkorb/) and click on "Mehrere Bestell-Nummern einfügen"

and copy paste the generated tables. there might be a problem with the length of the line. There is no problem deleting some references (like R1 R2 R4) for shorting the line.
