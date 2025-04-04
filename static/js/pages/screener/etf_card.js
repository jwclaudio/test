class EtfCard {
    constructor(etf) {
        this.etf = etf;
        this.element = this.createCard();
        this.setupEventListeners();
    }

    createCard() {
        const card = document.createElement('div');
        card.className = 'etf-card';
        card.innerHTML = `
            <div class="etf-header">
                <div class="etf-symbol">${this.etf.symbol}</div>
                <div class="etf-name">${this.etf.name}</div>
            </div>
            <div class="etf-metrics">
                <div class="metric-item">
                    <span class="metric-label">Asset Class</span>
                    <span class="metric-value">${this.etf.asset_class}</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Region</span>
                    <span class="metric-value">${this.etf.region}</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">AUM</span>
                    <span class="metric-value">${this.etf.aum}</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Expense Ratio</span>
                    <span class="metric-value">${this.etf.expense_ratio}</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Price</span>
                    <span class="metric-value">$${this.etf.price}</span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">YTD Return</span>
                    <span class="metric-value ${this.etf.ytd_return >= 0 ? 'positive' : 'negative'}">
                        ${this.etf.ytd_return >= 0 ? '+' : ''}${this.etf.ytd_return}%
                    </span>
                </div>
            </div>
            <div class="etf-actions">
                <button class="compare-btn">
                    <i class="fas fa-chart-line"></i>
                    Compare
                </button>
            </div>
        `;
        return card;
    }

    setupEventListeners() {
        const compareBtn = this.element.querySelector('.compare-btn');
        compareBtn.addEventListener('click', () => this.handleCompareClick());
    }

    handleCompareClick() {
        const isSelected = window.compareEtfs.comparisonList.some(e => e.symbol === this.etf.symbol);
        const compareBtn = this.element.querySelector('.compare-btn');
        
        if (isSelected) {
            compareBtn.classList.remove('selected');
        } else {
            compareBtn.classList.add('selected');
        }
        
        document.dispatchEvent(new CustomEvent('toggleComparison', { detail: this.etf }));
    }

    getElement() {
        return this.element;
    }
}

export default EtfCard; 