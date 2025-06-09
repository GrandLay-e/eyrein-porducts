from my_api import api
from src import main, functions, CONST

choice = input("1 ou 2")
if choice =="1":
    print("API")
    api.app.run(debug=True)
elif choice =="2":
    print("GET")
    main.get_data_from_web()
else:
    print("FAUX")