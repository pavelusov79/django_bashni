from django.contrib import admin
from django.contrib.admin import StackedInline

from property.models import City, BuildingObjects, MainPhotos, BuildingPhotos, \
    ObjectDocuments, CheckObjectReadiness, CheckTermsPassKeys, Property, Flats, BuildMonths


admin.site.register(Property)


@admin.register(Flats)
class FlatsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('fl_type',)}
    list_display = ('fl_type', 'fk_object', 'fl_num', 'fl_price', 'build_num')
    list_filter = ('fk_object', 'fl_type', 'fl_decor', 'fl_status')
    search_fields = ('id',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'city_slug': ('city_name',)}
    list_display = ('city_name', 'city_code')


class MainPhotosInline(StackedInline):
    model = MainPhotos
    extra = 0


class BuildingPhotosInline(StackedInline):
    model = BuildingPhotos
    extra = 0


class ObjectsDocumentsInline(StackedInline):
    model = ObjectDocuments
    extra = 0


class CheckObjectReadinessInline(StackedInline):
    model = CheckObjectReadiness
    extra = 0


class CheckTermsPassKeysInline(StackedInline):
    model = CheckTermsPassKeys
    extra = 0


class BuildingMonthsInline(StackedInline):
    model = BuildMonths
    extra = 0


@admin.register(BuildMonths)
class BuildMonthsAdmin(admin.ModelAdmin):
    list_display = ('build_month', 'fk_property',)
    list_filter = ('fk_property',)
    inlines = [BuildingPhotosInline]


@admin.register(BuildingObjects)
class BuildingObjectsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'city')
    list_filter = ('city', 'has_flats', 'build_stage', 'property_class', 'wall', 'decoration')
    search_fields = ('name__startswith',)
    inlines = [MainPhotosInline, BuildingMonthsInline, ObjectsDocumentsInline,
               CheckObjectReadinessInline, CheckTermsPassKeysInline]



