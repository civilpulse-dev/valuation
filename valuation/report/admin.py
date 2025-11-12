from django.contrib import admin
from django.utils.html import format_html
from .models import Valuation, Property, Owner, Plot, VisitingTeam

@admin.register(Valuation)
class ValuationAdmin(admin.ModelAdmin):
    list_display = ('report_number', 'bank_name', 'borrower_name', 'val_date', 'properties_count', 'created_at')
    list_filter = ('val_date', 'bank_name', 'created_at')
    search_fields = ('report_number', 'bank_name', 'borrower_name', 'bank_ref_no')
    date_hierarchy = 'val_date'
    ordering = ('-val_date',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('report_number', 'val_date')
        }),
        ('Bank Details', {
            'fields': ('bank_name', 'bank_branch', 'bank_address', 'bank_req_date', 'bank_ref_no')
        }),
        ('Borrower Details', {
            'fields': ('borrower_name', 'borrower_address', 'borrower_contact', 'borrower_pan', 'borrower_citizenship')
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def properties_count(self, obj):
        return obj.properties.count()
    properties_count.short_description = 'Properties'

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'municipality', 'valuation_link', 'owners_count', 'plots_count', 'total_value_display', 'created_at')
    list_filter = ('district', 'land_type', 'created_at')
    search_fields = ('name', 'district', 'municipality', 'address')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('valuation', 'name', 'land_type')
        }),
        ('Location Details', {
            'fields': ('address', 'district', 'municipality', 'ward_no')
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def valuation_link(self, obj):
        return format_html('<a href="/admin/report/valuation/{}/change/">{}</a>', 
                          obj.valuation.id, obj.valuation.report_number)
    valuation_link.short_description = 'Valuation Report'
    
    def owners_count(self, obj):
        return obj.owners.count()
    owners_count.short_description = 'Owners'
    
    def plots_count(self, obj):
        return obj.plots.count()
    plots_count.short_description = 'Plots'
    
    def total_value_display(self, obj):
        return f"Rs. {obj.total_value:,.2f}" if obj.total_value else "Rs. 0.00"
    total_value_display.short_description = 'Total Value'

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'property_link', 'contact_number', 'citizenship_number', 'pan_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'contact_number', 'citizenship_number', 'pan_number', 'property__name')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Owner Information', {
            'fields': ('property', 'name', 'contact_number')
        }),
        ('Identification', {
            'fields': ('citizenship_number', 'pan_number')
        }),
        ('Address', {
            'fields': ('address',)
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def property_link(self, obj):
        return format_html('<a href="/admin/report/property/{}/change/">{}</a>', 
                          obj.property.id, obj.property.name)
    property_link.short_description = 'Property'

@admin.register(Plot)
class PlotAdmin(admin.ModelAdmin):
    list_display = ('plot_number', 'property_link', 'area_display', 'market_rate_display', 'fair_market_value_display', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('plot_number', 'sheet_number', 'property__name')
    readonly_fields = ('created_at', 'area_sqft', 'area_sqmt', 'gov_value', 'market_value', 'fair_market_value')
    
    fieldsets = (
        ('Plot Identification', {
            'fields': ('property', 'plot_number', 'sheet_number')
        }),
        ('Area Measurement - Ropani System (Hilly)', {
            'fields': ('ropani', 'ana', 'paisa', 'dam'),
            'classes': ('collapse',)
        }),
        ('Area Measurement - Bigha System (Terai)', {
            'fields': ('bigha', 'kattha', 'dhur'),
            'classes': ('collapse',)
        }),
        ('International Units (Auto-calculated)', {
            'fields': ('area_sqft', 'area_sqmt'),
            'classes': ('collapse',)
        }),
        ('Valuation Rates', {
            'fields': ('gov_rate_per_sqft', 'market_rate_per_sqft')
        }),
        ('Calculated Values (Auto-calculated)', {
            'fields': ('gov_value', 'market_value', 'fair_market_value'),
            'classes': ('collapse',)
        }),
        ('Boundaries', {
            'fields': ('north_boundary', 'south_boundary', 'east_boundary', 'west_boundary'),
            'classes': ('collapse',)
        }),
        ('Additional Details', {
            'fields': ('remarks',),
            'classes': ('collapse',)
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def property_link(self, obj):
        return format_html('<a href="/admin/report/property/{}/change/">{}</a>', 
                          obj.property.id, obj.property.name)
    property_link.short_description = 'Property'
    
    def area_display(self, obj):
        return obj.get_area_display()
    area_display.short_description = 'Area'
    
    def market_rate_display(self, obj):
        return f"Rs. {obj.market_rate_per_sqft:,.2f}/sq.ft" if obj.market_rate_per_sqft else "-"
    market_rate_display.short_description = 'Market Rate'
    
    def fair_market_value_display(self, obj):
        return f"Rs. {obj.fair_market_value:,.2f}" if obj.fair_market_value else "Rs. 0.00"
    fair_market_value_display.short_description = 'Fair Market Value'
    
    # Custom save method to ensure calculations are done
    def save_model(self, request, obj, form, change):
        obj.calculate_areas()
        obj.calculate_valuations()
        super().save_model(request, obj, form, change)

@admin.register(VisitingTeam)
class VisitingTeamAdmin(admin.ModelAdmin):
    list_display = ('member_name', 'designation', 'valuation_link', 'contact_number', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('member_name', 'designation', 'valuation__report_number')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Team Member Information', {
            'fields': ('valuation', 'member_name', 'designation', 'contact_number')
        }),
        ('System Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def valuation_link(self, obj):
        return format_html('<a href="/admin/report/valuation/{}/change/">{}</a>', 
                          obj.valuation.id, obj.valuation.report_number)
    valuation_link.short_description = 'Valuation Report'

# Custom Admin Site Header and Title
admin.site.site_header = 'Nepali Land Valuation System Administration'
admin.site.site_title = 'Valuation System Admin'
admin.site.index_title = 'Valuation System Management'


# Custom admin actions
def calculate_all_valuations(modeladmin, request, queryset):
    """Admin action to recalculate all valuations for selected plots"""
    for plot in queryset:
        plot.calculate_areas()
        plot.calculate_valuations()
        plot.save()
    modeladmin.message_user(request, f"Recalculated valuations for {queryset.count()} plots.")

calculate_all_valuations.short_description = "Recalculate valuations for selected plots"

# Add the action to PlotAdmin
PlotAdmin.actions = [calculate_all_valuations]