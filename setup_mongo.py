import os

from pymongo import MongoClient


def setup_mongo():
    menu_data = [
        {
            "name": "Hamburger",
            "category": "Entree",
            "price": 10
        },
        {
            "name": "Chicken Sandwich",
            "category": "Entree",
            "price": 8
        },
        {
            "name": "Fries",
            "category": "Side",
            "price": 2
        },
        {
            "name": "Salad",
            "category": "Side",
            "price": 3
        },
        {
            "name": "Coke",
            "category": "",
            "price": 2
        },
        {
            "name": "Sweet Tea",
            "category": "",
            "price": 2
        },
        {
            "name": "Milkshake",
            "category": "Drink",
            "price": 6
        }
    ]

    to_continue = input("請確認是否是第一次執行此 command，若多次執行會導致資料庫中有重複的資料，如果確定要繼續執行，請輸入 yes： ")
    if to_continue != "yes":
        print("輸入值不是 yes，結束執行")
        return
    client = MongoClient(host=os.getenv("MONGO_ENDPOINT"))
    client.order_system.menu.insert_many(menu_data)
    print("資料匯入成功！")


if __name__ == "__main__":
    setup_mongo()
