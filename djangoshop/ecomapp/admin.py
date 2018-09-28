from django.contrib import admin
from .models import Category, Brand, Product, CartItem, Cart, Order

def make_payed(modeladmin, request, queryset):
    queryset.update(status='Оплачен')
make_payed.short_description = "Пометить как оплаченные"

class OrderAdmin(admin.ModelAdmin):
    list_filter = ['status']
    actions = [make_payed]
class TitlePrepopulated(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Category, TitlePrepopulated)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)


