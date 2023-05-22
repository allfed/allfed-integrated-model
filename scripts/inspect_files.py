import inspect
import animal_populations

def get_functions_and_classes(module):
    functions = []
    classes = []
    
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj):
            functions.append(name)
        elif inspect.isclass(obj):
            classes.append(name)
            class_members = inspect.getmembers(obj)
            for member_name, member_obj in class_members:
                if inspect.isfunction(member_obj):
                    full_name = f"{name}.{member_name}"
                    functions.append(full_name)
    
    return functions, classes

# Assuming your animal_populations.py module is in the same directory
### CHNAGE THIS TO YOUR OWN PATH ###
module = animal_populations

functions, classes = get_functions_and_classes(module)

print("Functions:")
for func in functions:
    print(func)

print("Classes:")
for cls in classes:
    print(cls)
