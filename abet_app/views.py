from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Employee, Asset
from django.utils.dateparse import parse_date


# Authentication Views
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid username or password."
            return render(request, 'abet_app/login.html', {'error': error})
    return render(request, 'abet_app/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard View
@login_required
def dashboard(request):
    employees = Employee.objects.all()
    return render(request, 'abet_app/dashboard.html', {'employees': employees})

# Employee Views
@login_required
def add_employee(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        department = request.POST['department']
        Employee.objects.create(name=name, email=email, department=department)
        return redirect('dashboard')
    return render(request, 'abet_app/employee_form.html', {'action': 'Add'})

@login_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        employee.name = request.POST['name']
        employee.email = request.POST['email']
        employee.department = request.POST['department']
        employee.save()
        return redirect('dashboard')
    return render(request, 'abet_app/employee_form.html', {'employee': employee, 'action': 'Edit'})

@login_required
def delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    employee.delete()
    return redirect('dashboard')

# Asset Views
@login_required
def view_assets(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    return render(request, 'abet_app/view_assets.html', {'employee': employee})


@login_required
def add_asset(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        print(request.POST)  # Debug print to verify POST data
        Asset.objects.create(
            employee=employee,
            asset_name=request.POST['asset_name'],
            asset_type=request.POST['asset_type'],
            serial_number=request.POST['serial_number'],
            assigned_date=request.POST['assigned_date']
        )
        return redirect('view_assets', employee_id=employee.id)
    return render(request, 'abet_app/asset_form.html', {'employee': employee, 'action': 'Add'})



@login_required
# def edit_asset(request, asset_id):
#     asset = get_object_or_404(Asset, id=asset_id)
#     if request.method == 'POST':
#         asset.asset_name = request.POST['asset_name']
#         asset.asset_type = request.POST['asset_type']
#         asset.serial_number = request.POST['serial_number']
#         asset.assigned_date = request.POST['assigned_date']
#         asset.save()
#         return redirect('view_assets', employee_id=asset.employee.id)
#     return render(request, 'abet_app/asset_form.html', {'asset': asset, 'employee': asset.employee, 'action': 'Edit'})


def edit_asset(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)

    if request.method == "POST":
        asset.asset_type = request.POST.get('asset_type', '').strip()
        asset.asset_name = request.POST.get('asset_name', '').strip()
        asset.serial_number = request.POST.get('serial_number', '').strip()
        assigned_date_str = request.POST.get('assigned_date', '').strip()

        if assigned_date_str == "":
            # Either set to None if your model allows null=True, blank=True
            asset.assigned_date = None
            # Or raise an error if date is required:
            # return render with error message (see below)
        else:
            assigned_date = parse_date(assigned_date_str)
            if not assigned_date:
                # Invalid date format, render form with error
                error = "Please enter a valid date in YYYY-MM-DD format."
                return render(request, 'abet_app/asset_form.html', {
                    'asset': asset,
                    'employee': asset.employee,
                    'error': error,
                    'asset_type': asset.asset_type,
                    'asset_name': asset.asset_name,
                    'serial_number': asset.serial_number,
                    'assigned_date': assigned_date_str,
                    'action': 'Edit',
                })
            asset.assigned_date = assigned_date

        asset.save()
        return redirect('view_assets', employee_id=asset.employee.id)

    return render(request, 'abet_app/asset_form.html', {
        'asset': asset,
        'employee': asset.employee,
        'action': 'Edit',
    })


@login_required


@login_required
def delete_asset(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    employee_id = asset.employee.id
    asset.delete()
    return redirect('view_assets', employee_id=employee_id)
