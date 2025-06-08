from django.contrib import admin

from .models import Product, Material, ProductMaterial, Warehouse


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code',)
    search_fields = ('name',)


class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class ProductMaterialAdmin(admin.ModelAdmin):
    list_display = ('product', 'material', 'quantity')
    search_fields = ('product', 'material')


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('material', 'remainder', 'price')
    search_fields = ('material',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(ProductMaterial, ProductMaterialAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
