from django.db import models
from django.urls import reverse
from datetime import date
from django.utils import timezone
from decimal import Decimal
from django.core.exceptions import ValidationError

class Valuation(models.Model):
    # Basic Information
    val_date = models.DateField(default=date.today, verbose_name="Valuation Date")
    report_number = models.CharField(max_length=50, unique=True, verbose_name="Report Number")
    
    # Bank Details
    bank_name = models.CharField(max_length=100, verbose_name="Bank Name")
    bank_branch = models.CharField(max_length=100, blank=True, verbose_name="Bank Branch")
    bank_address = models.TextField(blank=True, verbose_name="Bank Address")
    bank_req_date = models.DateField(blank=True, null=True, verbose_name="Bank Request Date")
    bank_ref_no = models.CharField(max_length=100, blank=True, verbose_name="Bank Reference No")
    
    # Borrower Details
    borrower_name = models.CharField(max_length=100, verbose_name="Borrower Name")
    borrower_address = models.TextField(blank=True, verbose_name="Borrower Address")
    borrower_contact = models.CharField(max_length=15, blank=True, verbose_name="Contact Number")
    borrower_pan = models.CharField(max_length=15, blank=True, verbose_name="PAN Number")
    borrower_citizenship = models.CharField(max_length=20, blank=True, verbose_name="Citizenship Number")
    
    # Auto-generated timestamp (remove from form)
    created_at = models.DateTimeField(auto_now_add=True)  # Changed to auto_now_add
    
    class Meta:
        verbose_name = "Valuation Report"
        verbose_name_plural = "Valuation Reports"
        ordering = ['-val_date']
    
    def __str__(self):
        return f"{self.report_number} - {self.bank_name}"
    
    def get_absolute_url(self):
        return reverse('report:valuation_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        if not self.report_number:
            # Auto-generate report number if not provided
            from datetime import datetime
            prefix = "VAL"
            year_month = datetime.now().strftime("%Y-%m")
            last_report = Valuation.objects.filter(
                report_number__startswith=f"{prefix}-{year_month}"
            ).order_by('-report_number').first()
            
            if last_report:
                try:
                    last_number = int(last_report.report_number.split('-')[-1])
                    new_number = last_number + 1
                except (ValueError, IndexError):
                    new_number = 1
            else:
                new_number = 1
                
            self.report_number = f"{prefix}-{year_month}-{new_number:04d}"
        
        super().save(*args, **kwargs)

        @property
        def total_valuation(self):
            """Calculate total valuation from all properties"""
            total = 0
            for property in self.properties.all():
                total += property.total_value
            return total

class Property(models.Model):
    valuation = models.ForeignKey(Valuation, on_delete=models.CASCADE, related_name='properties')
    name = models.CharField(max_length=100, verbose_name="Property Name")
    address = models.TextField(verbose_name="Property Address")
    district = models.CharField(max_length=50, verbose_name="District")
    municipality = models.CharField(max_length=50, blank=True, verbose_name="Municipality")
    ward_no = models.IntegerField(default=1, verbose_name="Ward Number")
    
    # Land Details
    land_type = models.CharField(max_length=20, choices=[
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('agricultural', 'Agricultural'),
        ('forest', 'Forest'),
        ('other', 'Other')
    ], default='residential')
    
    # Auto-generated timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Properties"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.district}"
    
    def get_absolute_url(self):
        return reverse('report:property_edit', kwargs={'pk': self.pk})
    
    @property
    def total_value(self):
        """Calculate total value from all plots"""
        return sum(plot.fair_market_value or 0 for plot in self.plots.all())
    
    @property
    def total_area_sqft(self):
        """Calculate total area in square feet"""
        return sum(plot.area_sqft or 0 for plot in self.plots.all())

class Owner(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='owners')
    name = models.CharField(max_length=100, verbose_name="Owner Name")
    address = models.TextField(blank=True, verbose_name="Owner Address")
    contact_number = models.CharField(max_length=15, blank=True, verbose_name="Contact Number")
    citizenship_number = models.CharField(max_length=20, blank=True, verbose_name="Citizenship Number")
    pan_number = models.CharField(max_length=15, blank=True, verbose_name="PAN Number")
    
    # Auto-generated timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Property Owners"
    
    def __str__(self):
        return self.name

class Plot(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='plots')
    
    # Plot Identification
    plot_number = models.CharField(max_length=20, verbose_name="Plot Number")
    sheet_number = models.CharField(max_length=20, blank=True, verbose_name="Sheet Number")
    
    # Area Measurement - Ropani System (Hilly)
    ropani = models.IntegerField(default=0, verbose_name="Ropani")
    ana = models.IntegerField(default=0, verbose_name="Ana")
    paisa = models.IntegerField(default=0, verbose_name="Paisa")
    dam = models.DecimalField(max_digits=6, decimal_places=4, default=0, verbose_name="Dam")
    
    # Area Measurement - Bigha System (Terai)
    bigha = models.IntegerField(default=0, verbose_name="Bigha")
    kattha = models.IntegerField(default=0, verbose_name="Kattha")
    dhur = models.IntegerField(default=0, verbose_name="Dhur")
    
    # International Units (Auto-calculated)
    area_sqft = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Area (Sq. Ft)")
    area_sqmt = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Area (Sq. M)")
    
    # Valuation Rates
    gov_rate_per_sqft = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Government Rate/Sq.Ft")
    market_rate_per_sqft = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Market Rate/Sq.Ft")
    
    # Calculated Values
    gov_value = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Government Value")
    market_value = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Market Value")
    fair_market_value = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Fair Market Value")
    
    # Boundaries
    north_boundary = models.CharField(max_length=100, blank=True, verbose_name="North Boundary")
    south_boundary = models.CharField(max_length=100, blank=True, verbose_name="South Boundary")
    east_boundary = models.CharField(max_length=100, blank=True, verbose_name="East Boundary")
    west_boundary = models.CharField(max_length=100, blank=True, verbose_name="West Boundary")
    
    # Additional Details
    remarks = models.TextField(blank=True, verbose_name="Remarks")
    
    # Auto-generated timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Land Plots"
        ordering = ['plot_number']
    
    def __str__(self):
        return f"Plot {self.plot_number} - {self.get_area_display()}"
    
    def clean(self):
        """Validate area measurements"""
        errors = {}
        
        # Ropani system validation
        if self.ana < 0 or self.ana > 15:
            errors['ana'] = 'Ana must be between 0 and 15'
        if self.paisa < 0 or self.paisa > 3:
            errors['paisa'] = 'Paisa must be between 0 and 3'
        if self.dam < 0 or self.dam > 4:
            errors['dam'] = 'Dam must be between 0 and 4'
        
        # Bigha system validation
        if self.kattha < 0 or self.kattha > 19:
            errors['kattha'] = 'Kattha must be between 0 and 19'
        if self.dhur < 0 or self.dhur > 19:
            errors['dhur'] = 'Dhur must be between 0 and 19'
        
        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.calculate_areas()
        self.calculate_valuations()
        super().save(*args, **kwargs)
    
    def calculate_areas(self):
        """Calculate area in square feet and square meters"""
        # Convert Ropani system to sq.ft (1 Ropani = 5476 sq.ft)
        ropani_sqft = (self.ropani * 5476) + (self.ana * 342.25) + (self.paisa * 85.56) + (float(self.dam) * 21.39)
        
        # Convert Bigha system to sq.ft (1 Bigha = 72900 sq.ft in Nepal)
        bigha_sqft = (self.bigha * 72900) + (self.kattha * 3645) + (self.dhur * 182.25)
        
        total_sqft = ropani_sqft + bigha_sqft
        self.area_sqft = Decimal(str(total_sqft))
        self.area_sqmt = Decimal(str(total_sqft * 0.092903))
    
    def calculate_valuations(self):
        """Calculate all valuation amounts"""
        if self.area_sqft > 0:
            self.gov_value = self.area_sqft * (self.gov_rate_per_sqft or 0)
            self.market_value = self.area_sqft * (self.market_rate_per_sqft or 0)
            
            # Fair market value (weighted average: 30% gov + 70% market)
            if self.gov_rate_per_sqft > 0 or self.market_rate_per_sqft > 0:
                weighted_rate = (self.gov_rate_per_sqft * Decimal('0.3')) + (self.market_rate_per_sqft * Decimal('0.7'))
                self.fair_market_value = self.area_sqft * weighted_rate
    
    def get_area_display(self):
        """Get formatted area display"""
        if self.ropani > 0 or self.ana > 0 or self.paisa > 0 or self.dam > 0:
            return f"{self.ropani}-{self.ana}-{self.paisa}-{self.dam} (R-A-P-D)"
        elif self.bigha > 0 or self.kattha > 0 or self.dhur > 0:
            return f"{self.bigha}-{self.kattha}-{self.dhur} (B-K-D)"
        else:
            return f"{self.area_sqft:,.2f} Sq.Ft"

class VisitingTeam(models.Model):
    valuation = models.ForeignKey(Valuation, on_delete=models.CASCADE, related_name='visiting_teams')
    member_name = models.CharField(max_length=100, verbose_name="Team Member Name")
    designation = models.CharField(max_length=100, verbose_name="Designation")
    contact_number = models.CharField(max_length=15, blank=True, verbose_name="Contact Number")
    
    # Auto-generated timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Visiting Team Member"
        verbose_name_plural = "Visiting Team Members"
    
    def __str__(self):
        return f"{self.member_name} - {self.designation}"