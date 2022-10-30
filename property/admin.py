from django.contrib import admin
from django.contrib.admin import StackedInline

from property.models import City, Buildings, MainPhotos, BuildingPhotos, \
    ObjectDocuments, CheckObjectReadiness, CheckTermsPassKeys, Property, \
    Flats, BuildMonths, RatingStar, Rating, Facilities, PropertyDecor, \
    PropertyDecorImages, PropertyFloorPlans, MediaFlats, PropertyFeeds

from main.models import YoutubeChannel


admin.site.register(Facilities)
admin.site.register(RatingStar)


@admin.register(MediaFlats)
class MediaFlatsAdmin(admin.ModelAdmin):
    list_display = ('fk_property', 'flat_choice')


@admin.register(PropertyFeeds)
class PropertyFeedsAdmin(admin.ModelAdmin):
    list_display = ('fk_property',)
    search_fields = ['fk_property__name__icontains']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('star', 'property', 'ip')


class ZhkName(admin.SimpleListFilter):
    title = 'Жилые комплексы'
    parameter_name = 'zhk'

    def lookups(self, request, model_admin):
        zhk = [i.fk_property for i in model_admin.model.objects.filter(fk_property__has_scraper=True).distinct('fk_property__name').order_by('fk_property__name')]
        return [(i.id, i.name) for i in zhk]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(fk_property=self.value())
        else:
            return queryset.all()


@admin.register(Flats)
class FlatsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('fl_type',)}
    list_display = ('fl_type', 'fk_property', 'fl_num', 'fl_price', 'build_num')
    list_filter = (ZhkName, 'fl_type', 'fl_decor', 'fl_status')
    search_fields = ('id',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'city_slug': ('city_name',)}
    list_display = ('city_name', 'city_code')


class MediaFlatsInline(StackedInline):
    model = MediaFlats
    extra = 0


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


class YoutubeChannelInline(StackedInline):
    model = YoutubeChannel
    extra = 0


class PropertyDecorImagesInline(StackedInline):
    model = PropertyDecorImages
    extra = 0


class PropertyFloorPlansInline(StackedInline):
    model = PropertyFloorPlans
    extra = 0


class PropertyFeedsInline(StackedInline):
    model = PropertyFeeds
    extra = 0


@admin.register(BuildMonths)
class BuildMonthsAdmin(admin.ModelAdmin):
    list_display = ('build_month', 'fk_building',)
    list_filter = ('fk_building',)
    inlines = [BuildingPhotosInline]


@admin.register(PropertyDecor)
class PropertyDecorAdmin(admin.ModelAdmin):
    list_display = ['decor', 'fk_property']
    list_filter = ['decor']
    search_fields = ['fk_property__icontains']
    inlines = [PropertyDecorImagesInline]


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'city', 'has_scraper')
    list_filter = ('city', 'has_scraper')
    search_fields = ('name__icontains', )
    inlines = [PropertyFeedsInline, YoutubeChannelInline, MediaFlatsInline]


@admin.register(Buildings)
class BuildingsAdmin(admin.ModelAdmin):
    list_display = ('num_dom', 'fk_property', 'start_date')
    list_filter = ('build_stage', 'property_class', 'wall', 'decoration', 'start_date')
    search_fields = ('fk_property__name__icontains',)
    inlines = [MainPhotosInline, BuildingMonthsInline, ObjectsDocumentsInline,
               CheckObjectReadinessInline, CheckTermsPassKeysInline, PropertyFloorPlansInline]



