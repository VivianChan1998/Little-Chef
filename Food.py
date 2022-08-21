class Food:
    def __init__(self, station_n):
        food_dict = {
            "BUN":{
                "name": "BUN",
                "instructions": "",
                "isPreped": True
            },
            "LETTUCE":{
                "name": "LETTUCE",
                "instructions": "chop",
                "isPreped": False
            },
            "TOMATO":{
                "name": "TOMATO",
                "instructions": "chop",
                "isPreped": False
            },
            "CHEESE":{
                "name": "CHEESE",
                "instructions": "chop",
                "isPreped": False
            },
            "MEAT":{
                "name": "MEAT",
                "instructions": "cook",
                "isPreped": False
            },
            "SPAGHETTI":{
                "name": "SPAGHETTI",
                "instructions": "cook",
                "isPreped": False
            },
        }

        def get_nth_key(dictionary, n=0):
            if n < 0:
                n += len(dictionary)
            for i, key in enumerate(dictionary.keys()):
                if i == n:
                    return key

        f = get_nth_key(food_dict, station_n-5)
        print(f)
        self.name = food_dict[f]['name']
        self.instructions = food_dict[f]['instructions']
        self.isPreped = food_dict[f]['isPreped']