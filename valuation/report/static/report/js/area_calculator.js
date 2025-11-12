// Area Calculator for Nepali Land Measurement Systems

class NepaliAreaCalculator {
    constructor() {
        this.conversionRates = {
            ropaniToSqft: 5476.00,
            anaToSqft: 342.25,
            paisaToSqft: 85.56,
            damToSqft: 21.39,
            bighaToSqft: 72900.00,
            katthaToSqft: 3645.00,
            dhurToSqft: 182.25
        };
        // Only initialize if we're on a page with area calculation fields
        if (this.hasAreaFields()) {
            this.init();
        }
    }
    
    hasAreaFields() {
        // Check if any area calculation fields exist on the page
        return document.getElementById('id_ropani') || 
               document.getElementById('id_bigha') || 
               document.getElementById('id_area_sqft');
    }
    
    init() {
        this.bindEvents();
        this.updateDisplay();
    }
    
    bindEvents() {
        // Ropani system inputs - only if they exist
        ['ropani', 'ana', 'paisa', 'dam'].forEach(field => {
            const element = document.getElementById(`id_${field}`);
            if (element) {
                element.addEventListener('input', () => this.calculateFromRopani());
            }
        });
        
        // Bigha system inputs - only if they exist
        ['bigha', 'kattha', 'dhur'].forEach(field => {
            const element = document.getElementById(`id_${field}`);
            if (element) {
                element.addEventListener('input', () => this.calculateFromBigha());
            }
        });
        
        // Direct area input - only if it exists
        const areaSqft = document.getElementById('id_area_sqft');
        if (areaSqft) {
            areaSqft.addEventListener('input', () => this.calculateFromSqft());
        }
    }
    
    calculateFromRopani() {
        const ropani = this.getFieldValue('ropani');
        const ana = this.getFieldValue('ana');
        const paisa = this.getFieldValue('paisa');
        const dam = this.getFieldValue('dam');
        
        const totalSqft = (ropani * this.conversionRates.ropaniToSqft) +
                         (ana * this.conversionRates.anaToSqft) +
                         (paisa * this.conversionRates.paisaToSqft) +
                         (dam * this.conversionRates.damToSqft);
        
        this.setFieldValue('area_sqft', totalSqft);
        this.setFieldValue('area_sqmt', totalSqft * 0.092903);
        this.updateDisplay();
    }
    
    calculateFromBigha() {
        const bigha = this.getFieldValue('bigha');
        const kattha = this.getFieldValue('kattha');
        const dhur = this.getFieldValue('dhur');
        
        const totalSqft = (bigha * this.conversionRates.bighaToSqft) +
                         (kattha * this.conversionRates.katthaToSqft) +
                         (dhur * this.conversionRates.dhurToSqft);
        
        this.setFieldValue('area_sqft', totalSqft);
        this.setFieldValue('area_sqmt', totalSqft * 0.092903);
        this.updateDisplay();
    }
    
    calculateFromSqft() {
        const areaSqft = this.getFieldValue('area_sqft');
        if (areaSqft > 0) {
            this.setFieldValue('area_sqmt', areaSqft * 0.092903);
            this.updateDisplay();
        }
    }
    
    getFieldValue(fieldName) {
        const element = document.getElementById(`id_${fieldName}`);
        return element ? parseFloat(element.value) || 0 : 0;
    }
    
    setFieldValue(fieldName, value) {
        const element = document.getElementById(`id_${fieldName}`);
        if (element) {
            element.value = value.toFixed(2);
        }
    }
    
    updateDisplay() {
        const displayElement = document.getElementById('area-calculator-display');
        if (!displayElement) return;
        
        const ropani = this.getFieldValue('ropani');
        const ana = this.getFieldValue('ana');
        const paisa = this.getFieldValue('paisa');
        const dam = this.getFieldValue('dam');
        const bigha = this.getFieldValue('bigha');
        const kattha = this.getFieldValue('kattha');
        const dhur = this.getFieldValue('dhur');
        const areaSqft = this.getFieldValue('area_sqft');
        const areaSqmt = this.getFieldValue('area_sqmt');
        
        let displayHTML = '<div class="calculated-values p-3 rounded">';
        displayHTML += '<h6><i class="fas fa-calculator me-2"></i>Area Calculation</h6>';
        
        if (ropani > 0 || ana > 0 || paisa > 0 || dam > 0) {
            displayHTML += `<p class="mb-1">Ropani System: ${ropani}-${ana}-${paisa}-${dam} (R-A-P-D)</p>`;
        }
        
        if (bigha > 0 || kattha > 0 || dhur > 0) {
            displayHTML += `<p class="mb-1">Bigha System: ${bigha}-${kattha}-${dhur} (B-K-D)</p>`;
        }
        
        displayHTML += `<p class="mb-1"><strong>Total Area: ${areaSqft.toLocaleString()} sq.ft (${areaSqmt.toLocaleString()} sq.m)</strong></p>`;
        displayHTML += '</div>';
        
        displayElement.innerHTML = displayHTML;
    }
    
    // Method to convert area to different systems
    convertArea(areaSqft, toSystem) {
        switch (toSystem) {
            case 'ropani':
                return this.sqftToRopani(areaSqft);
            case 'bigha':
                return this.sqftToBigha(areaSqft);
            default:
                return { sqft: areaSqft, sqmt: areaSqft * 0.092903 };
        }
    }
    
    sqftToRopani(areaSqft) {
        const ropani = Math.floor(areaSqft / this.conversionRates.ropaniToSqft);
        const remaining = areaSqft % this.conversionRates.ropaniToSqft;
        const ana = Math.floor(remaining / this.conversionRates.anaToSqft);
        const remaining2 = remaining % this.conversionRates.anaToSqft;
        const paisa = Math.floor(remaining2 / this.conversionRates.paisaToSqft);
        const dam = (remaining2 % this.conversionRates.paisaToSqft) / this.conversionRates.damToSqft;
        
        return {
            ropani: ropani,
            ana: ana,
            paisa: paisa,
            dam: parseFloat(dam.toFixed(4))
        };
    }
    
    sqftToBigha(areaSqft) {
        const bigha = Math.floor(areaSqft / this.conversionRates.bighaToSqft);
        const remaining = areaSqft % this.conversionRates.bighaToSqft;
        const kattha = Math.floor(remaining / this.conversionRates.katthaToSqft);
        const dhur = (remaining % this.conversionRates.katthaToSqft) / this.conversionRates.dhurToSqft;
        
        return {
            bigha: bigha,
            kattha: kattha,
            dhur: parseFloat(dhur.toFixed(2))
        };
    }
}

// Initialize calculator only if area fields exist
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('id_ropani') || document.getElementById('id_bigha')) {
        window.areaCalculator = new NepaliAreaCalculator();
    }
});

// Utility function for quick area conversion
function convertNepaliArea(areaSqft, fromSystem, toSystem) {
    const calculator = new NepaliAreaCalculator();
    return calculator.convertArea(areaSqft, toSystem);
}