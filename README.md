Структура исходного кода:

```
src -+- main.py
     |
     -- data.db
     |
     -- modules -+- module1 -+- module1.module.py
     |           |           |
     |           -- ...      -- module1.keyboard.py
     |                       |
     |                       -- module1.db.py
     |
     -- admin -+- admin_tool1
               |
               -- ...
```

Создать новый модуль:

```bash
python src/admin/create_module.py module_name
```
