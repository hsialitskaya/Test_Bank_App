# 💰💲 MoneyManager 💲💰

MoneyManager is a Python-based application designed to manage personal and corporate accounts while handling a variety of financial transactions. The app allows users to create and organize accounts, and seamlessly manage incoming, outgoing, and express transactions. With a focus on testing and ensuring accuracy, MoneyManager helps verify the functionality of financial operations in a controlled, non-UI environment. The goal of the app is to provide a robust and reliable solution for developers and testers looking to ensure the stability and precision of financial systems.

# 💻 Technologies Used

MoneyManager is built using the following technologies:

📍 Python   
📍 Gherkin   
📍 unittest  
📍 parameterized  
📍 flask (for any future API)  
📍 behave (for behavior-driven development and testing)  
📍 requests (for making HTTP requests)  
📍 unittest_assertions (for enhanced assertion methods in unit tests)  
📍 pymongo (for interacting with MongoDB for data storage and retrieval)  

These technologies ensure that MoneyManager is reliable, scalable, and thoroughly tested.


# 🏁 Getting Started

To get started with the MoneyManager, follow these steps:

1️⃣ Clone the Repository  

Download the repository to your local machine by running the following command in your terminal:  
```bash
git clone https://github.com/hsialitskaya/Test_Bank_App.git
```

2️⃣ Install Dependencies
Ensure you have Python installed on your system. Then, navigate to the project directory and install the required dependencies:

```bash
pip install -r requirements.txt
```


## 👩🏼‍🔬 How to Test  
Here’s how to run various types of tests for the MoneyManager application:  

1️⃣ Unit Tests    
To run unit tests and measure coverage, follow these steps:  

1. From the main directory, run the following command to execute the tests with coverage:   
```bash
python3 -m coverage run -m unittest
```

2. To check the coverage report, use:
```bash
python3 -m coverage report
```

2️⃣ API Tests  
To test the API:

1. Start Flask by running the following command from the main directory:
```bash
python3 -m flask --app=app/api.py run
```

2. After Flask is running, execute the API tests with:
```bash
python3 -m unittest app/api_test/*
```


3️⃣ BDD Tests  
To test Behavior-Driven Development (BDD) scenarios:

1. Start Flask by running the following command from the main directory:
```bash
python3 -m flask --app=app/api.py run
```

2. After Flask is running, execute the BDD tests with:
```bash
python3 -m behave app/features
```


4️⃣ Performance Tests  
To test the performance of the application:

1. Start Flask by running the following command from the main directory:
```bash
python3 -m flask --app=app/api.py run
```

2. After Flask is running, execute the performance tests with:
```bash
python3 -m unittest app/performance/performanceTests.py
```

These steps ensure comprehensive testing across all aspects of your application, including unit, API, BDD, and performance tests.


## License
MoneyManager is licensed under the MIT License. See [LICENSE](https://github.com/hsialitskaya/Test_Bank_App/blob/main/LICENSE) for more information.


Happy coding and enjoy testing with MoneyManager! 🎉
