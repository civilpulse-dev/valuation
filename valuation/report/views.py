from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Q
from .models import Valuation, Property, Owner, Plot, VisitingTeam
from .forms import ValuationForm, PropertyForm, OwnerForm, PlotForm
from django.forms import inlineformset_factory
from django.db.models import Sum

# Create formsets
OwnerFormSet = inlineformset_factory(
    Property, Owner, form=OwnerForm, 
    extra=1, can_delete=True, fields='__all__'
)

PlotFormSet = inlineformset_factory(
    Property, Plot, form=PlotForm,
    extra=1, can_delete=True, fields='__all__'
)

def dashboard(request):
    """Main dashboard view"""
    stats = {
        'valuations': Valuation.objects.count(),
        'properties': Property.objects.count(),
        'owners': Owner.objects.count(),
        'plots': Plot.objects.count(),
    }
    return render(request, 'report/dashboard.html', {'stats': stats})

def valuation_list(request):
    """List all valuation reports"""
    valuations = Valuation.objects.all().order_by('-val_date')
    return render(request, 'report/valuation_list.html', {'valuations': valuations})

def valuation_create(request):
    """Create new valuation report"""
    if request.method == 'POST':
        form = ValuationForm(request.POST)
        if form.is_valid():
            valuation = form.save()
            messages.success(request, 'Valuation report created successfully!')
            return redirect('report:valuation_detail', pk=valuation.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ValuationForm()
    
    return render(request, 'report/valuation_create.html', {'form': form})

def valuation_detail(request, pk):
    """View valuation report details"""
    valuation = get_object_or_404(
        Valuation.objects.prefetch_related('properties__owners', 'properties__plots'), 
        pk=pk
    )
    return render(request, 'report/valuation_detail.html', {'valuation': valuation})

def property_list(request):
    """List all properties"""
    properties = Property.objects.select_related('valuation').annotate(
        owner_count=Count('owners'),
        plot_count=Count('plots'),
        # Use annotation to calculate total value
        total_value_sum=Sum('plots__fair_market_value')
    )
    
    return render(request, 'report/property_list.html', {'properties': properties})
    
def plot_list(request):
    """List all land plots"""
    plots = Plot.objects.select_related('property__valuation')
    return render(request, 'report/plot_list.html', {'plots': plots})

def owner_list(request):
    """List all property owners"""
    owners = Owner.objects.select_related('property__valuation')
    return render(request, 'report/owner_list.html', {'owners': owners})

def property_add(request, valuation_pk):
    """Add a new property to a valuation"""
    valuation = get_object_or_404(Valuation, pk=valuation_pk)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.valuation = valuation
            property.save()
            messages.success(request, f'Property "{property.name}" added successfully!')
            return redirect('report:property_edit', pk=property.pk)
    else:
        form = PropertyForm()
    
    return render(request, 'report/property_add.html', {
        'form': form,
        'valuation': valuation
    })

def property_edit(request, pk):
    """Edit property with owners and plots"""
    property_instance = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        owner_formset = OwnerFormSet(request.POST, instance=property_instance, prefix='owners')
        plot_formset = PlotFormSet(request.POST, instance=property_instance, prefix='plots')
        
        if owner_formset.is_valid() and plot_formset.is_valid():
            owner_formset.save()
            plot_formset.save()
            messages.success(request, 'Property updated successfully!')
            return redirect('report:valuation_detail', pk=property_instance.valuation.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        owner_formset = OwnerFormSet(instance=property_instance, prefix='owners')
        plot_formset = PlotFormSet(instance=property_instance, prefix='plots')
    
    return render(request, 'report/property_edit.html', {
        'property_instance': property_instance,
        'owner_formset': owner_formset,
        'plot_formset': plot_formset,
    })