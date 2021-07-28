from pulp import LpMaximize, LpProblem, LpVariable


def create_lp_model():
    # Create the model to optimize
    model = LpProblem(name="optimization_nutrition", sense=LpMaximize)

    # Initialize the variable to maximize
    z = LpVariable(name="minimum_value_nutrition", lowBound=0)

    # For the moment definition of variables # Latter importation of variables
    # Variables for food
    S = LpVariable(name="Seaweed", lowBound=0)
    G = LpVariable(name="Greenhouse_crops", lowBound=0)
    R = LpVariable(name="Ruminants", lowBound=0)
    C = LpVariable(name="Outdoor_crop", lowBound=0)
    B = LpVariable(name="Single_cell_protein", lowBound=0)
    W = LpVariable(name="Sugar", lowBound=0)

    # Variables for resources
    NG = LpVariable(name="Natural_Gas", lowBound=0)
    Pla = LpVariable(name="Plastic", lowBound=0)
    A = LpVariable(name="Area_Hectares", lowBound=0)
    FE = LpVariable(name="Nitrogen_Fertilizer", lowBound=0)
    FI = LpVariable(name="Fibers", lowBound=0)
    WO = LpVariable(name="Wood", lowBound=0)

    # Variables for nutrition
    Fat = LpVariable(name="Fat", lowBound=0)
    CA = LpVariable(name="Calories", lowBound=0)
    P = LpVariable(name="Protein", lowBound=0)

    # When starting dynamic programmation
    # StoredF = LpVariable(name="Sugar", lowBound=0)

    # Implementation constrains
    # Constraint for food_resources
    model += (S <= FI*10, "Seaweed_constraint")
    model += (G <= Pla*10.6, "Greenhouses_constraint_plastic")
    model += (G <= FE*5, "Greenhouses_constraint_fertilizer")
    model += (R <= A*100, "Ruminant_constraint_area")
    model += (C <= FE*0.016983, "Crop_outdoor_constraint_fertilizer")
    model += (C <= A*0.000111, "Crop_outdoor_constraint_area")
    model += (B <= NG*2, "Single_cell_protein_constraint_Nitrogen")
    model += (B <= FE*0.15, "Single_cell_protein_constraint_Fertilizer")


    # Constraint resources
    model += (NG <= 100000, "Natural_Gas_constraint")
    model += (Pla <= 500, "Plastic_constraint")
    model += (A <= 5*pow(10, 8), "Area_constraint_fertilizer")
    model += (FE == NG*0.73, "Fertilizer_constraint_Nitrogen")
    model += (FI <= 100, "Fiber_constraint")
    model += (WO <= 100000, "Wood_constraint")

    # Constraint nutrition_food

    model += (CA == 100*S + 500*G + 2000*R + 1556*C + 5200*B + 2000*W, "Nutrition_CA")
    model += (Fat == 0.1*S + 20*G + 1000*R + 31*C + 90*B + 100*W, "Nutrition_Fat")
    model += (P == 10*S + 5*G + 30*R + 33*C + 600*B + 20*W, "Nutrition_Protein")

    # Constraint for linearisation minimum function

    model += (z*2386*0.15 <= Fat, "Min_Nutrition_Fat")
    model += (z*2386 <= CA, "Min_Nutrition_Calories")
    model += (z*60 <= P, "Min_Nutrition_Proteins")

    obj_func = z
    model += obj_func

    return model


def run():
    model = create_lp_model()
    status = model.solve()
    print(f"objective: {model.objective.value()}")
    for var in model.variables():
        print(f"{var.name}: {var.value()}")


if __name__ == '__main__':
    run()


