from django.db import models
from django.contrib.auth.models import User

# Default Categories (optional, this could also be seeded in the database on app startup)
class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories', null=True, blank=True)  # Allows both default and user-specific categories

    def __str__(self):
        return self.name
    
    class Meta:
        # Ensure the combination of user and name is unique
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_user_category')
        ]


# Subcategory model which relates to a specific Category
class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subcategories', null=True, blank=True)  # User-specific subcategories

    def __str__(self):
        return self.name

    class Meta:
        # Ensure the combination of category and name is unique
        constraints = [
            models.UniqueConstraint(fields=['category', 'name'], name='unique_category_subcategory')
        ]

# Transactions for managing expenses/incomes
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense')
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField() 
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} ({self.date})"
