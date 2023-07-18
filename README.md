![alt text](https://github.com/exPriceD/UniPeptides-PyQt-App/blob/master/static/images/logo_for_readme.png)
# [UniPeptides](https://unipeptides.ru)
**UniPeptides** - web service for searching biologically active peptides in proteins

The main function of the site is to search for peptides in proteins. It is carried out by parsing proteins from the site uniprot.org through the API and by searching for the peptides you have introduced in the amino acid chain of the protein

Web service:
+ Allows you to analyze the amino acid sequences of collagens and other proteins available in the publicly available UniProtKB database, find the desired peptides in them, and output the result in the form of a table with user-defined parameters;
+ Includes a database of biologically active peptides found in collagens. With the ability to add information about new peptides by the user.
+ Allows the user to create a personal account to save all the results of the analysis of the search for peptides.

**Prospects for the development of the web service.**\
It is planned to add user information to the registration (full name, organization, identifiers WoS; Scopus; Research ID; ORCID, contacts); expansion of information about peptides in the database; creation of a forum for peptide researchers. The prospects of the software part of the site: improving the interface, mail messages; switching to React; site optimization; account confirmation during registration; mobile application.

# Installation
`git clone https://github.com/exPriceD/UniPeptides-Website.git`\
\
`pip install requirements.txt`

`Setup config.py`

# Stack
- **Flask**
- **MySQL (SQLite in repo)**
- **HTML, CSS**
- **JavaScript, jQuery**
- **Asyncio, Aiohttp**
- **Openpyxl**

# Database

**SQLite** `application.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"`

**MySQL** `application.config['SQLALCHEMY_DATABASE_URI'] = "mysql://user:pass!@host/database_name"`


<p align="center">
  <img src="https://github.com/exPriceD/UniPeptides-Website/blob/master/static/images/database.drawio.svg"/>
</p>

# Interface
![alt text](https://github.com/exPriceD/UniPeptides-Website/blob/master/static/images/prew.png)

## Menu
![alt text](https://github.com/exPriceD/UniPeptides-Website/blob/master/static/images/menu.png)

## Search for peptides
![alt text](https://github.com/exPriceD/UniPeptides-Website/blob/master/static/images/search.png)
### Result example 
![alt text](https://github.com/exPriceD/UniPeptides-Website/blob/master/static/images/result.png)

## Peptides database
![alt text](https://github.com/exPriceD/UniPeptides-Website/blob/master/static/images/database.png)
![alt text](https://github.com/exPriceD/UniPeptides-Website/blob/master/static/images/add_form.png)

## Account
![alt text](https://github.com/exPriceD/UniPeptides-Website/blob/master/static/images/account.png)

#Authorization pages
![alt text](https://github.com/exPriceD/UniPeptides-Website/blob/master/static/images/login.png)
![alt text](https://github.com/exPriceD/UniPeptides-Website/blob/master/static/images/register.png)

## Only for editors:
![alt text](https://github.com/exPriceD/UniPeptides-Website/blob/master/static/images/panel_db.png)
![alt text](https://github.com/exPriceD/UniPeptides-Website/blob/master/static/images/panel_req.png)

## Errors page
![alt text](https://github.com/exPriceD/UniPeptides-Website/blob/master/static/images/errors.png)

## Mail messages
![alt text](https://github.com/exPriceD/UniPeptides-Website/blob/master/static/images/mail.png)
