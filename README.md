# pyBomQuote

This tool helps you to search the pages de.farnell.com and de.rs-online.com for the parts
listet in your bill of materials. It collects data like ordercode, price, availability and
URL for each product. This information helps you to select the supplier for each product.
At the end you can export cart tables which can be uploaded directly to the supplier pages to
be added to your shopping cart.

![Mainwindow Screenshot](docs/mainwindow.png?raw=true "Mainwindow Screenshot")

##How to use pBomQuote
pyBomQuote accepts *.csv tables with the pipesymbol '|' as seperator with the folling format:

| Number | quantity | quantity | Reference | Manufacturer Part Number | Manufacturer | LibRef | Footprint | Description

where Number and Libref are ignored.

An example BOM file looks like:

```
7|1|C8|T491B476K010A|Kemet|T491B476K010A|CAP_POL_3528_TANTALB_HIGHDENS|47u/10V/Tanatal Package B
6|1|C9|GRM188R61H105KAALD|Murata|GRM188R61H105KAALD|cap_0603_highdens|CAP CER 0603 1u 50V X5R 10%
5|3|C12, C18, C21|C1005X5R0J475M050BC|TDK|C1005X5R0J475M050BC|cap_0402_highdens|CAP CER 0402 4u7 6V3 X5R 20%
```



