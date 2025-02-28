from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .models import Category, Subcategory, Transaction
import matplotlib.pyplot as plt
import io
import urllib, base64
from django.db.models import Sum

# Create your views here.


def register_view(request):
    print("register_view_Called")
    print(request.method)
    if request.method == "POST":
        print("POST method called")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(first_name, last_name, username, password)
        try:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=username,
                date_joined=datetime.now(),
            )
            user.set_password(password)
            user.save()
            print("user saved successfully")
            messages.info(request, "Account created successfully")
            return redirect("/finance/register/")
        except Exception as e:
            print(e)
            messages.error(request, str(e))
            return redirect("/finance/register/")

    return render(request, "auth/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not User.objects.filter(username=username).exists():
            messages.error(request, str("Username not found"))
            return redirect("/finance/login/")

        user = authenticate(username=username, password=password)
        if not user:
            messages.error(request, str("Invalid Password"))
            return redirect("/finance/login/")
        else:
            login(request, user)
            return redirect("/finance/dashboard")
    return render(request, "auth/login.html")


@login_required(login_url="/finance/dashboard")
def dashboard_view(request):
    my_transactions = Transaction.objects.filter(user=request.user)
    expenses = my_transactions.filter(transaction_type="expense")

    # Group expenses by category
    category_expenses = expenses.values("category__name").annotate(
        total_amount=Sum("amount")
    )

    # Prepare data for the pie chart
    categories = [category["category__name"] for category in category_expenses]
    amounts = [category["total_amount"] for category in category_expenses]

    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=90)
    ax.axis("equal")  # Equal aspect ratio ensures the pie chart is a circle.

    # Save the plot to a BytesIO object and encode it to base64 for embedding in HTML
    image_buffer = io.BytesIO()
    plt.savefig(image_buffer, format="png")
    image_buffer.seek(0)
    image_data = base64.b64encode(image_buffer.read()).decode("utf-8")
    return render(
        request,
        "dashboard/user_profile.html",
        {"my_transactions": my_transactions, "pie_chart": image_data},
    )


@login_required(login_url="/finance/add_category")
def add_category_subcategory(request):
    if request.method == "POST":
        print("here")
        # Handle Add Category Form Submission
        if "add_category" in request.POST:
            category_name = request.POST.get("category_name")
            print("adding catgory", category_name)
            if category_name:
                # Create a new category for the logged-in user
                try:
                    Category.objects.create(name=category_name, user=request.user)
                    messages.info(
                        request,
                        f"{category_name} - Category added !!",
                        extra_tags="category",
                    )
                except Exception as e:
                    messages.error(request, str(e), extra_tags="category")
                return redirect("/finance/add_category")  # Redirect to the same page

        # Handle Add Subcategory Form Submission
        elif "add_subcategory" in request.POST:
            print("Adding Subcategory")
            subcategory_name = request.POST.get("subcategory_name")
            category_id = request.POST.get("category")
            print("adding catgory", subcategory_name)
            if subcategory_name and category_id:
                category = Category.objects.get(id=category_id, user=request.user)
                # Create a new subcategory for the logged-in user
                try:
                    Subcategory.objects.create(
                        name=subcategory_name, category=category, user=request.user
                    )
                    messages.info(
                        request,
                        f"{subcategory_name} - Sub-category added !!",
                        extra_tags="subcategory",
                    )
                except Exception as e:
                    messages.error(request, str(e), extra_tags="subcategory")
                return redirect("/finance/add_category")  # Redirect to the same page

    # Fetch all categories created by the logged-in user for the subcategory dropdown
    categories = Category.objects.filter(user=request.user)
    return render(request, "dashboard/add_category.html", {"categories": categories})


@login_required(login_url="/finance/add_transaction")
def add_transaction(request):
    if request.method == "POST":
        transaction_type = request.POST.get("transaction_type")
        amount = request.POST.get("amount")
        category_id = request.POST.get("category")
        subcategory_id = request.POST.get("subcategory")
        description = request.POST.get("description")
        date = request.POST.get("date")

        category = Category.objects.get(id=category_id)
        subcategory = (
            Subcategory.objects.get(id=subcategory_id) if subcategory_id else None
        )

        Transaction.objects.create(
            transaction_type=transaction_type,
            amount=amount,
            category=category,
            subcategory=subcategory,
            user=request.user,
            description=description,
            date=date,
        )
        return render(request, "dashboard/add_transaction.html")

    categories = Category.objects.filter(user=request.user)
    subcategories = Subcategory.objects.filter(category__user=request.user)

    return render(
        request,
        "dashboard/add_transaction.html",
        {"categories": categories, "subcategories": subcategories},
    )


def logout_view(request):
    logout(request)
    return redirect("/finance/login/")
