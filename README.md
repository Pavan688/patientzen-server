# PatientZen Server
Server for PatientZen


This is the client for the [PatientZen-Client](https://github.com/Pavan688/PatientZen-Client)


## Installation
Follow the steps below to download and run this project on your computer
- [ ] Client is required for full functionality. [View client repo here](https://github.com/Pavan688/PatientZen-Client)
- [ ] Clone this repository
- [ ] From server directory, run "pipenv install"
- [ ] Make sure to be in a virtual environment. "pipenv shell"
- [ ] Run this code:
```bash
rm db.sqlite3
rm -rf ./patientzenapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations patientzenapi
python3 manage.py migrate patientzenapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata patients
python3 manage.py loaddata providers
python3 manage.py loaddata insurances
python3 manage.py loaddata offices
python3 manage.py loaddata appointments
python3 manage.py loaddata records
```
- [ ] Run "python manage.py runserver"




## Pavankumar Patel
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Pavan688)
[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/pavankumar-patel-916597265/)


## Tech Stack

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
