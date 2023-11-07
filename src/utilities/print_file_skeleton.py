import ast
import astor


def extract_functions_and_classes(node, indent=""):
    if isinstance(node, ast.FunctionDef):
        print(indent + f"Function: {node.name}")

    if isinstance(node, ast.ClassDef):
        print(indent + f"Class: {node.name}")

        # for class_node in ast.walk(node):
        #     if isinstance(class_node, ast.FunctionDef):
        #         print(indent + '    ' + f"Function inside class {node.name}: {class_node.name}")

    for child in ast.iter_child_nodes(node):
        extract_functions_and_classes(child, indent + "    ")


if __name__ == "__main__":
    # Replace with the path to your Python file
    file_path = "/Users/kevin/Documents/ProgrammingIsFun/ALLFED/Integrated/allfed-integrated-model/src/food_system/animal_populations.py"

    with open(file_path, "r") as file:
        file_contents = file.read()

    parsed_ast = ast.parse(file_contents)
    extract_functions_and_classes(parsed_ast)
