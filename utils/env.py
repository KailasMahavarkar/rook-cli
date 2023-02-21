import json
import os

# get path
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
STORAGE_PATH = os.path.join(ROOT_PATH, "storage")
CONFIG_PATH = os.path.join(STORAGE_PATH, 'config.json')


if not os.path.isdir(STORAGE_PATH):
    os.mkdir(STORAGE_PATH)
    
if not os.path.isfile(CONFIG_PATH):
    with open(CONFIG_PATH, 'w') as f:
        json.dump({}, f)
        

def setKey(key: str, value: str):
    with open(CONFIG_PATH, 'r') as f:
        data = json.load(f)
        data[key] = value
    
        os.environ[key] = str(value)

        with open(CONFIG_PATH, 'w') as f:
            json.dump(data, f)
    return True


def parse(key: str):
    # check if key can be string or int or boolean
    if key == 'True':
        return True
    elif key == 'False':
        return False
    elif key == 'None':
        return None
    
    try:
        return int(key)
    except ValueError:
        try:
            return float(key)
        except ValueError:
            try:
                return str(key)
            except ValueError:
                return None


    



def getKey(key) -> str:
    if os.environ.get(key) is not None:
        return parse(os.environ[key])
    else:
        with open(CONFIG_PATH, 'r') as f:
            data = json.load(f)
            
            # check if key exist
            if key in data:
                setKey(key=key, value=data[key])
                return parse(data[key])
            else:
                return None


def deleteKey(key: str):
    if os.environ.get(key) is not None:
        os.environ[key] = ""
        with open(CONFIG_PATH, 'r') as f:
            data = json.load(f)
            data.pop(key)
            with open(CONFIG_PATH, 'w') as f:
                json.dump(data, f)
            return True
    else:
        return False


if __name__ == '__main__':
    setKey("zeno", False)
    print(getKey("zeno"), type(getKey("zeno")))

    # getResult = getKey("zeno")
    # print("get -->", getResult)
    # delResult = deleteKey('zeno')
    # print("delete -->", delResult)
