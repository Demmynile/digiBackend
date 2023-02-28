from django.contrib import admin
from .models import User,Product,Vendor,Buyer,Order,ShippingAddress,Category,SuperCategory,SubCategory,Items,PermanentAddress
from import_export.admin import ImportExportModelAdmin

# from import_export.widgets import ManyToManyWidget

# Register your models here.
admin.site.register(Product)
admin.site.register(Vendor)
admin.site.register(Order)
admin.site.register(User)
admin.site.register(Buyer)
admin.site.register(ShippingAddress)
admin.site.register(PermanentAddress)

# admin.site.register(SuperCategory)
# admin.site.register(Category)
# admin.site.register(SubCategory)
# admin.site.register(Items)


@admin.register(Items)
class ViewAdmin(ImportExportModelAdmin):
    list_display=('name','status','id_child_id')


@admin.register(SubCategory)
class ViewAdmin(ImportExportModelAdmin):
    list_display=('name','status','id_parent_id')

@admin.register(Category)
class ViewAdmin(ImportExportModelAdmin):
    list_display=('name','status','id_superparent_id')

@admin.register(SuperCategory)
class ViewAdmin(ImportExportModelAdmin):
    list_display=('name','status')


