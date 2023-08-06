import json

class db():
    def __init__(self, database_name):
        self.database_name = database_name
        with open(database_name, "a") as f:
            try:
                json.load(f)
            except:
                f.write("[]")
            return
    
    def write(self, key, value):
        with open(self.database_name, "a") as f:
            js = json.load(f)
        #CHECK IF KEY EXISTS
        for x in js:
            if x["key"] == key:
                x["value"] = value
                return True
        js.append({"key": key, "value": value})
        with open(self.database_name, "w") as f:
            json.dump(js, f)
        return True

    def read(self, key):
        with open(self.database_name, "a") as f:
            js = json.load(f)
        for x in js:
            if x["key"] == key:
                return x["value"]