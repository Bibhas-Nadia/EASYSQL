# EASYSQL: A Smart SQL Query Suggestion Tool

EASYSQL is a terminal-based tool designed to help beginners write correct SQL queries by offering real-time, schema-based suggestions and corrections. It simplifies learning SQL by guiding users through syntax, structure, and query construction using dynamic, context-aware suggestions.

---

## 🔍 Features

- 🧠 **Real-time SQL Suggestions**: Offers context-aware recommendations based on live schema and user input.
- 🛠 **Automatic Query Correction**: Fixes syntax errors like missing semicolons, unmatched parentheses, and misused keywords.
- 📊 **Live Database Validation**: Suggests actual table and field names by connecting to a MySQL database.
- 🎓 **Beginner-Friendly**: Built for students and learners to understand and improve SQL writing.
- ⚙️ **Terminal-Based**: Lightweight and cross-platform, works on Windows CMD, Bash, and ZSH terminals.

---

## 📸 Screenshots

> 📌 **Suggestion Prompting**  
Real-time keyword and clause suggestions as the user types.  
![Suggestion Prompting](Images/detect_exack_words.png)

> 📌 **Schema-Aware Completion**  
Displays relevant table/column names pulled from the connected database.  
![Schema Completion](Images/fifth.png)

> 📌 **Automatic Corrections**  
Corrects syntax issues like missing semicolons or unmatched parentheses.  
![Auto Correction](Images/correction_img.png)

---

## 📚 Dataset

- 1400+ pre-constructed queries based on SQL operations.
  - `SELECT`: 300+  
  - `INSERT`: 150+  
  - `UPDATE`: 110+  
  - `DELETE`: 120+  
- Query ontology and knowledge graph built manually.
- Tools used: Protégé, ChatGPT for refinement and structure.

---

## 🧪 Technical Specifications

- **Languages**: Python 3.6+
- **Libraries**:
  - `prompt_toolkit`
  - `rich`
  - `os`, `re`, `pytest-shutil`
- **Supported OS**:
  - Windows 10/11
  - Ubuntu 20.04+, Manjaro Linux 25.0.0
- **Databases**:
  - MySQL
  - MariaDB 11.7.2
- **Minimum Requirements**:
  - 2 GB RAM
  - Python 3.6 or later

---

## 🏗 Architecture Overview

High-level architecture showing user interaction, suggestion engine, and database connection.  
![Architecture](Images/use_case.png)

---

## 🧩 Methodology

Includes use case diagrams, suggestion process logic, and backend workflow.  
![Workflow](Images/overal_steps..png)

Also prove basic suggestions 
![Correction](Images/correction.png)
---

## 🧱 Limitations

- Only supports **MySQL/MariaDB**.
- Dependent on pre-defined ontology.
- Does not currently support **GUI** or **natural language input**.

---

##  Future Scope

- PostgreSQL and Oracle DB support
- Natural language to SQL conversion
- Machine learning–based suggestion engine
- GUI version for non-terminal users

---


##  Installation

* Downlaod the repository

```bash
git clone https://github.com/Bibhas-Das/EASYSQL.git
```

Or downlaod teh Zip file

* Go to EASYSQL/install folder

```bash
cd EASYSQL/install
```

* There install.sh file si there just run it

```bash
sudo chmod +x install.sh
./install.sh
```

* It will automaticly copy all nessary file and folders to /opt/easysql folder  and configured

* Just make sure that you have already a mysql/mariadb server install in your system and has a already a database.

* [Optional] If you face trouble to install mysql/mariadb then go to help folder and run the mysql_setup.sh

```bash
sudo sh mysql_setup.sh
```
It will downlaod , setup and import a dummy database

* Provide the database user name, password, and database name

* Then It is ready to run

```bash
easysql.sh
```

* You can run this application from anywhere by your terminal with your curent user
* All details and logs will be store on that particular folder only you can easyly visit teh location "/opt/easysql"
---

#  Uninstallation

* To uninstallation just remove the easysql folder from your system. 

```bash
sudo -rm /opt/easysql
```

* And remove the line form your currect shell rc file

 
 - First check your shell 
 ```bash
 echo $SHELL
 ``` 
- As example if you use bash shell, then open ~/.bashrc file form any text editor

```bash
nano ~/.bashrc
```

- Remove the line from last "export PATH=/opt/easysql:$PATH"

- Then Ctrl+S for save
- And Ctrl+X for exit

* Now It is totaly uninstall from your system



## 🙏 Acknowledgements

Developed under the guidance of **Dr. Sayani Mondal**, Assistant Professor, Department of Computer Science, Sister Nivedita University.

Special thanks to our families, peers, and academic mentors for their support and encouragement throughout this project.

---

## 📄 License

Copyright (c) 2025 Team EASYSQL (Sister Nivedita University)

This project is made available for **academic demonstration purposes only**.  
Redistribution, modification, or commercial use is **strictly prohibited** without prior written permission.

For licensing inquiries, please contact the authors.


---

## 📫 Contact

For questions, suggestions, or collaboration, please open an [Issue](https://github.com/yourusername/EASYSQL/issues) or contact any team member via GitHub.

