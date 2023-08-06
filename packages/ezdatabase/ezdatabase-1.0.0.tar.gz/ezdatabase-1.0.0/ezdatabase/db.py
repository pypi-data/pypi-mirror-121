import json

class db():
    def __init__(self, database_name):
        """Initializes the Database

        Args:
            database_name (str): "The Name of the Database with ending"

        Returns:
            bool: "True if the Database was initialized"
        """
        self.database_name = database_name
        try:
            with open(database_name, "r") as f:
                json.load(f)
        except:
            with open(database_name, "w") as s:
                s.write("[]")
                s.close()
        return True
    
    def write(self, key, value):
        """Writes / Updates a key to the Database

        Args:
            key (str, int, float): "The Key to get written"
        
        Returns:
            Bool: "True if the key was written / updated"
        """
        with open(self.database_name, "r") as f:
            js = json.load(f)
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
        """Read Key from the Database

        Args:
            key (str, int, float): "The Key to get read"

        Returns:
            str, int, float: "The Value of the Key"
        """
        with open(self.database_name, "r") as f:
            js = json.load(f)
        for x in js:
            if x["key"] == key:
                return x["value"]
        return None

    def delete(self, key):
        """Deletes a key from the Database

        Args:
            key (str, int, float): "The Key to get Deleted"

        Returns:
            Bool: "True if the key was deleted"
        """
        deleted = False
        with open(self.database_name, "r") as f:
            js = json.load(f)
        for x in js:
            if x["key"] == key:
                js.remove(x)
                deleted = True
        with open(self.database_name, "w") as f:
            json.dump(js, f)
        return deleted