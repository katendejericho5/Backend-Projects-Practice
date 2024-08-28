from django.shortcuts import render

def convert_length(value, from_unit, to_unit):
    conversion_factors = {
        'millimeter': 1,
        'centimeter': 10,
        'meter': 1000,
        'kilometer': 1000000,
        'inch': 25.4,
        'foot': 304.8,
        'yard': 914.4,
        'mile': 1609344,
    }
    value_in_mm = value * conversion_factors[from_unit]
    return value_in_mm / conversion_factors[to_unit]

def convert_weight(value, from_unit, to_unit):
    conversion_factors = {
        'milligram': 1,
        'gram': 1000,
        'kilogram': 1000000,
        'ounce': 28349.5,
        'pound': 453592,
    }
    value_in_mg = value * conversion_factors[from_unit]
    return value_in_mg / conversion_factors[to_unit]

def convert_temperature(value, from_unit, to_unit):
    if from_unit == 'Celsius' and to_unit == 'Fahrenheit':
        return (value * 9/5) + 32
    elif from_unit == 'Fahrenheit' and to_unit == 'Celsius':
        return (value - 32) * 5/9
    elif from_unit == 'Celsius' and to_unit == 'Kelvin':
        return value + 273.15
    elif from_unit == 'Kelvin' and to_unit == 'Celsius':
        return value - 273.15
    elif from_unit == 'Fahrenheit' and to_unit == 'Kelvin':
        return (value - 32) * 5/9 + 273.15
    elif from_unit == 'Kelvin' and to_unit == 'Fahrenheit':
        return (value - 273.15) * 9/5 + 32
    return value


def length_converter(request):
    if request.method == 'POST':
        value_str = request.POST.get('value')
        from_unit = request.POST.get('from_unit')
        to_unit = request.POST.get('to_unit')
        
        try:
            # Validate and convert the value
            value = float(value_str)
            # Validate units
            valid_units = ['millimeter', 'centimeter', 'meter', 'kilometer', 'inch', 'foot', 'yard', 'mile']
            if from_unit not in valid_units or to_unit not in valid_units:
                raise ValueError("Invalid unit selected")

            converted_value = convert_length(value, from_unit, to_unit)
            return render(request, 'converter/length.html', {'converted_value': converted_value})
        
        except ValueError as e:
            # Handle invalid value or unit
            error_message = f"Error: {e}" if str(e) else "Invalid number entered. Please enter a valid number."
            return render(request, 'converter/length.html', {'error_message': error_message})

    return render(request, 'converter/length.html')


def weight_converter(request):
    if request.method == 'POST':
        value_str = request.POST.get('value')
        from_unit = request.POST.get('from_unit')
        to_unit = request.POST.get('to_unit')
        
        try:
            # Validate and convert the value
            value = float(value_str)
            # Validate units
            valid_units = ['milligram', 'gram', 'kilogram', 'ounce', 'pound']
            if from_unit not in valid_units or to_unit not in valid_units:
                raise ValueError("Invalid unit selected")

            converted_value = convert_weight(value, from_unit, to_unit)
            return render(request, 'converter/weight.html', {'converted_value': converted_value})

        except ValueError as e:
            # Handle invalid value or unit
            error_message = f"Error: {e}" if str(e) else "Invalid number entered. Please enter a valid number."
            return render(request, 'converter/weight.html', {'error_message': error_message})

    return render(request, 'converter/weight.html')


def temperature_converter(request):
    if request.method == 'POST':
        value_str = request.POST.get('value')
        from_unit = request.POST.get('from_unit')
        to_unit = request.POST.get('to_unit')
        
        try:
            # Validate and convert the value
            value = float(value_str)
            # Validate units
            valid_units = ['celsius', 'fahrenheit', 'kelvin']
            if from_unit not in valid_units or to_unit not in valid_units:
                raise ValueError("Invalid unit selected")

            converted_value = convert_temperature(value, from_unit, to_unit)
            return render(request, 'converter/temperature.html', {'converted_value': converted_value})

        except ValueError as e:
            # Handle invalid value or unit
            error_message = f"Error: {e}" if str(e) else "Invalid number entered. Please enter a valid number."
            return render(request, 'converter/temperature.html', {'error_message': 'Invalid input entered. Please enter a valid number.'})

    return render(request, 'converter/temperature.html')