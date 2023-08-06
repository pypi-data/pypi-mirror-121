# Simple Config
 Simple Attribute saving manager


## Installation

```bash
pip install simconf
```

## Documentation
### Init
```python
from SimConf import SimConf
config = SimConf(filename, default_atr, ensure_ascii, load_conf)
```
#### filename
```python
filename = "filename"
  (create filename.json)

filename = "folder/filename"
  (create filename.json in folder)
```

#### default_atr
```python
default_atr = {"arg0": 0, "arg1": 1 ...}
default_atr = ["arg0", "arg1" ...]
default_atr = {"a": {"b": [],},} etс
```

#### ensure_ascii
 Standard json attribute
```python
ensure_ascii = bool()
```

#### load_conf
  if true, loads values from file, if there is no file, uses default_atr,
  if false, uses default_atr
```python
load_conf = bool()
```

### Use

#### Get arg
```python
arg = config["arg"]
```

#### Set arg and create new
```python
config["arg"] = args
config["new"] = args
```

#### Set default value
```python
config.set_default() #use default_atr
```

#### Print in console all saves
```python
config.print_all()
```

### Support
 - **Telegramm** https://t.me/Rahazb
 - **Email** bokon2014@yandex.ru
