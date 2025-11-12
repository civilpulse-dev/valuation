// Dynamic Forms JavaScript for Nepali Land Valuation System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize only if we're on a page with plot forms
    initializePlotCalculators();
    initializeFormEnhancements();
});

function initializePlotCalculators() {
    // Area Calculation Functions
    function calculateAreaFromRopani() {
        const ropaniField = document.getElementById('id_ropani');
        const anaField = document.getElementById('id_ana');
        const paisaField = document.getElementById('id_paisa');
        const damField = document.getElementById('id_dam');
        
        if (!ropaniField || !anaField || !paisaField || !damField) return;
        
        const ropani = parseFloat(ropaniField.value) || 0;
        const ana = parseFloat(anaField.value) || 0;
        const paisa = parseFloat(paisaField.value) || 0;
        const dam = parseFloat(damField.value) || 0;
        
        // 1 Ropani = 5476 sq.ft, 1 Ana = 342.25 sq.ft, 1 Paisa = 85.56 sq.ft, 1 Dam = 21.39 sq.ft
        const totalSqft = (ropani * 5476) + (ana * 342.25) + (paisa * 85.56) + (dam * 21.39);
        
        if (totalSqft > 0) {
            const areaSqftField = document.getElementById('id_area_sqft');
            const areaSqmtField = document.getElementById('id_area_sqmt');
            
            if (areaSqftField) areaSqftField.value = totalSqft.toFixed(2);
            if (areaSqmtField) areaSqmtField.value = (totalSqft * 0.092903).toFixed(2);
            
            calculateValuation();
        }
    }
    
    function calculateAreaFromBigha() {
        const bighaField = document.getElementById('id_bigha');
        const katthaField = document.getElementById('id_kattha');
        const dhurField = document.getElementById('id_dhur');
        
        if (!bighaField || !katthaField || !dhurField) return;
        
        const bigha = parseFloat(bighaField.value) || 0;
        const kattha = parseFloat(katthaField.value) || 0;
        const dhur = parseFloat(dhurField.value) || 0;
        
        // 1 Bigha = 72900 sq.ft, 1 Kattha = 3645 sq.ft, 1 Dhur = 182.25 sq.ft
        const totalSqft = (bigha * 72900) + (kattha * 3645) + (dhur * 182.25);
        
        if (totalSqft > 0) {
            const areaSqftField = document.getElementById('id_area_sqft');
            const areaSqmtField = document.getElementById('id_area_sqmt');
            
            if (areaSqftField) areaSqftField.value = totalSqft.toFixed(2);
            if (areaSqmtField) areaSqmtField.value = (totalSqft * 0.092903).toFixed(2);
            
            calculateValuation();
        }
    }
    
    function calculateValuation() {
        const areaSqftField = document.getElementById('id_area_sqft');
        const marketRateField = document.getElementById('id_market_rate_per_sqft');
        const fairMarketValueField = document.getElementById('id_fair_market_value');
        
        // Check if all required fields exist
        if (!areaSqftField || !marketRateField || !fairMarketValueField) return;
        
        const areaSqft = parseFloat(areaSqftField.value) || 0;
        const marketRate = parseFloat(marketRateField.value) || 0;
        
        if (areaSqft > 0 && marketRate > 0) {
            const fairMarketValue = areaSqft * marketRate;
            fairMarketValueField.value = fairMarketValue.toFixed(2);
            
            // Update display if exists
            const displayElement = document.getElementById('valuation-display');
            if (displayElement) {
                displayElement.innerHTML = `
                    <div class="alert alert-info">
                        <h6>Valuation Summary</h6>
                        <p class="mb-1">Area: ${areaSqft.toLocaleString()} sq.ft</p>
                        <p class="mb-1">Market Rate: Rs. ${marketRate.toLocaleString()}/sq.ft</p>
                        <p class="mb-0 fw-bold">Fair Market Value: Rs. ${fairMarketValue.toLocaleString()}</p>
                    </div>
                `;
            }
        }
    }
    
    // Event Listeners for Area Calculation - only if fields exist
    const ropaniFields = ['id_ropani', 'id_ana', 'id_paisa', 'id_dam'];
    const bighaFields = ['id_bigha', 'id_kattha', 'id_dhur'];
    
    ropaniFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('input', calculateAreaFromRopani);
        }
    });
    
    bighaFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (field) {
            field.addEventListener('input', calculateAreaFromBigha);
        }
    });
    
    // Market Rate Change Listener - only if field exists
    const marketRateField = document.getElementById('id_market_rate_per_sqft');
    if (marketRateField) {
        marketRateField.addEventListener('input', calculateValuation);
    }
    
    // Direct Area Input Listener - only if field exists
    const areaSqftField = document.getElementById('id_area_sqft');
    if (areaSqftField) {
        areaSqftField.addEventListener('input', calculateValuation);
    }
}

function initializeFormEnhancements() {
    // Form Validation for Nepali Measurements
    function validateNepaliMeasurements() {
        const anaField = document.getElementById('id_ana');
        const paisaField = document.getElementById('id_paisa');
        const damField = document.getElementById('id_dam');
        const katthaField = document.getElementById('id_kattha');
        const dhurField = document.getElementById('id_dhur');
        
        // Only validate if these fields exist (we're on a plot form page)
        if (!anaField && !paisaField && !damField && !katthaField && !dhurField) {
            return []; // No errors if fields don't exist
        }
        
        const ana = anaField ? parseInt(anaField.value) || 0 : 0;
        const paisa = paisaField ? parseInt(paisaField.value) || 0 : 0;
        const dam = damField ? parseFloat(damField.value) || 0 : 0;
        const kattha = katthaField ? parseInt(katthaField.value) || 0 : 0;
        const dhur = dhurField ? parseInt(dhurField.value) || 0 : 0;
        
        let errors = [];
        
        if (ana < 0 || ana > 15) {
            errors.push('Ana must be between 0 and 15');
        }
        if (paisa < 0 || paisa > 3) {
            errors.push('Paisa must be between 0 and 3');
        }
        if (dam < 0 || dam > 4) {
            errors.push('Dam must be between 0 and 4');
        }
        if (kattha < 0 || kattha > 19) {
            errors.push('Kattha must be between 0 and 19');
        }
        if (dhur < 0 || dhur > 19) {
            errors.push('Dhur must be between 0 and 19');
        }
        
        return errors;
    }
    
    // Form Submission Handler - only for forms with Nepali measurements
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const errors = validateNepaliMeasurements();
            if (errors.length > 0) {
                e.preventDefault();
                alert('Please correct the following errors:\n\n' + errors.join('\n'));
            }
        });
    });
    
    // Auto-format Currency Fields
    const currencyFields = document.querySelectorAll('input[type="number"][step="0.01"]');
    currencyFields.forEach(field => {
        field.addEventListener('blur', function() {
            if (this.value && !isNaN(this.value)) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    });
    
    // Input validation styling for all forms
    const inputs = document.querySelectorAll('.form-control');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value.trim() !== '') {
                this.classList.add('is-valid');
            } else if (this.required) {
                this.classList.add('is-invalid');
            }
        });
        
        input.addEventListener('input', function() {
            this.classList.remove('is-invalid', 'is-valid');
        });
    });
    
    // Auto-generate report number suggestion for valuation forms
    const reportNumberField = document.getElementById('id_report_number');
    if (reportNumberField) {
        reportNumberField.addEventListener('focus', function() {
            if (!this.value) {
                const now = new Date();
                const suggestion = `VAL-${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
                this.placeholder = suggestion + '-XXXX';
            }
        });
    }
    
    // Responsive Table Enhancement
    function makeTablesResponsive() {
        const tables = document.querySelectorAll('table');
        tables.forEach(table => {
            if (table.offsetWidth > table.parentElement.offsetWidth) {
                table.parentElement.classList.add('table-responsive');
            }
        });
    }
    
    // Initialize on load
    makeTablesResponsive();
    
    // Re-run on window resize
    window.addEventListener('resize', makeTablesResponsive);
}

// Utility Functions - Safe to use anywhere
// Check if ValuationUtils already exists before declaring it
if (typeof ValuationUtils === 'undefined') {
    window.ValuationUtils = {
        // Convert Ropani to Square Feet
        ropaniToSqft: function(ropani, ana, paisa, dam) {
            return (ropani * 5476) + (ana * 342.25) + (paisa * 85.56) + (dam * 21.39);
        },
        
        // Convert Bigha to Square Feet
        bighaToSqft: function(bigha, kattha, dhur) {
            return (bigha * 72900) + (kattha * 3645) + (dhur * 182.25);
        },
        
        // Calculate Fair Market Value
        calculateFMV: function(areaSqft, marketRate) {
            return areaSqft * marketRate;
        },
        
        // Format Nepali Currency
        formatCurrency: function(amount) {
            if (!amount && amount !== 0) return 'Rs. 0.00';
            return 'Rs. ' + parseFloat(amount).toLocaleString('en-IN', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
        },
        
        // Validate Area Measurements
        validateMeasurements: function(measurements) {
            const errors = [];
            
            if (measurements.ana !== undefined && (measurements.ana < 0 || measurements.ana > 15)) {
                errors.push('Ana must be between 0 and 15');
            }
            if (measurements.paisa !== undefined && (measurements.paisa < 0 || measurements.paisa > 3)) {
                errors.push('Paisa must be between 0 and 3');
            }
            if (measurements.dam !== undefined && (measurements.dam < 0 || measurements.dam > 4)) {
                errors.push('Dam must be between 0 and 4');
            }
            if (measurements.kattha !== undefined && (measurements.kattha < 0 || measurements.kattha > 19)) {
                errors.push('Kattha must be between 0 and 19');
            }
            if (measurements.dhur !== undefined && (measurements.dhur < 0 || measurements.dhur > 19)) {
                errors.push('Dhur must be between 0 and 19');
            }
            
            return errors;
        }
    };
}