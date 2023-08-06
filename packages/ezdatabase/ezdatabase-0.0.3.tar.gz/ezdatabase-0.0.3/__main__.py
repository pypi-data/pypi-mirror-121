import json

class db():
    def __init__(self, database_name):
        self.database_name = database_name
        try:
            with open(database_name, "r") as f:
                json.load(f)
        except:
            with open(database_name, "w") as s:
                s.write("[]")
                s.close()
        return
    
    def write(self, key, value):
        with open(self.database_name, "r") as f:
            js = json.load(f)
        #CHECK IF KEY EXISTS
        for x in js:
            if x["key"] == key:
                x["value"] = value
                with open(self.database_name, "w") as f:
                    json.dump(js, f)
                return True
        js.append({"key": key, "value": value})
        with open(self.database_name, "w") as f:
            json.dump(js, f)
        return True

    def read(self, key):
        with open(self.database_name, "r") as f:
            js = json.load(f)
        for x in js:
            if x["key"] == key:
                return x["value"]

    def delete(self, key):
        with open(self.database_name, "r") as f:
            js = json.load(f)
        for x in js:
            if x["key"] == key:
                js.remove(x)
        with open(self.database_name, "w") as f:
            json.dump(js, f)