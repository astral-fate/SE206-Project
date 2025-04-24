def inspect_form_fields(form):
    """
    Helper function to inspect form fields and their choices
    Place this in a utility file and import it where needed
    """
    print("Inspecting form fields:")
    for field_name, field in form._fields.items():
        if hasattr(field, 'choices'):
            print(f"Field: {field_name}, Choices: {field.choices}")
            if field.choices is None:
                print(f"WARNING: Field {field_name} has None choices")
    return

# To use this in your route:
# from debug_form import inspect_form_fields
# inspect_form_fields(form)
