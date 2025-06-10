from my_api import api
from src.CONST import *
from src.functions import *

if len(api.all_products) == 0:
    logging.info("No products found. Please check the JSON file.")
    data = get_data_from_web()
    if data:
        api.all_products = json_to_object(JSON_FILE)
        api.formatted_products = format_all_data(api.all_products)
    else:
        logging.error("Failed to retrieve data from the web. Exiting.")
        exit(1)

else:
    print("Server running at http://localhost:8000")
    api.app.run(debug=True, host='localhost', port=8000)