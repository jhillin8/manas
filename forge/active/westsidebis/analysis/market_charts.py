import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Chart 1: Income Distribution by Neighborhood
def chart1_income_distribution():
    plt.figure(figsize=(10, 6))
    neighborhoods = ['Venice', 'Santa Monica', 'Brentwood']
    median_income = [67647, 109739, 150000]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    bars = plt.bar(neighborhoods, median_income, color=colors)
    plt.title('Median Household Income by Neighborhood', fontsize=16, fontweight='bold')
    plt.ylabel('Income ($)', fontsize=12)
    plt.xlabel('Neighborhood', fontsize=12)
    
    for bar, income in zip(bars, median_income):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2000,
                f'${income:,}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.show()

# Chart 2: Business Density Comparison
def chart2_business_density():
    plt.figure(figsize=(10, 6))
    data = {
        'Santa Monica': 1158,
        'Venice': 450,
        'Brentwood': 150
    }
    
    plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90,
            colors=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    plt.title('Business Density (per sq mile)', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()

# Chart 3: Customer Spending Archetypes
def chart3_customer_archetypes():
    plt.figure(figsize=(12, 8))
    archetypes = ['Tech Elite', 'Wellness Warrior', 'Beach Local', 'Tourist Explorer', 'Creative Class']
    spending_percentage = [25, 20, 18, 22, 15]
    annual_spend = [8500, 6200, 4800, 1200, 3200]
    
    x = np.arange(len(archetypes))
    width = 0.35
    
    fig, ax1 = plt.subplots(figsize=(12, 8))
    ax2 = ax1.twinx()
    
    bars1 = ax1.bar(x - width/2, spending_percentage, width, label='% of Total Spending', color='#FF6B6B')
    bars2 = ax2.bar(x + width/2, annual_spend, width, label='Annual Spend ($)', color='#4ECDC4')
    
    ax1.set_xlabel('Customer Archetype', fontsize=12)
    ax1.set_ylabel('% of Total Spending', fontsize=12)
    ax2.set_ylabel('Annual Spend per Customer ($)', fontsize=12)
    ax1.set_title('Customer Spending Patterns by Archetype', fontsize=16, fontweight='bold')
    
    ax1.set_xticks(x)
    ax1.set_xticklabels(archetypes, rotation=45, ha='right')
    
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    
    plt.tight_layout()
    plt.show()

# Chart 4: Growth Sectors Heatmap
def chart4_growth_sectors():
    plt.figure(figsize=(10, 8))
    sectors = ['Cannabis', 'Digital Health', 'Sustainable', 'Plant-Based', 'E-commerce', 'Wellness Tech', 'Experience']
    neighborhoods = ['Venice', 'Santa Monica', 'Brentwood']
    
    # Growth rates by sector and neighborhood
    growth_data = np.array([
        [45, 25, 10],  # Cannabis
        [20, 38, 30],  # Digital Health
        [32, 30, 20],  # Sustainable
        [35, 28, 25],  # Plant-Based
        [25, 30, 15],  # E-commerce
        [20, 35, 25],  # Wellness Tech
        [40, 25, 15]   # Experience
    ])
    
    sns.heatmap(growth_data, annot=True, fmt='d', cmap='YlOrRd', 
                xticklabels=neighborhoods, yticklabels=sectors,
                cbar_kws={'label': 'Growth Rate (%)'})
    plt.title('Growth Sectors by Neighborhood (Annual %)', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()

# Chart 5: Price Premium by Area
def chart5_price_premium():
    plt.figure(figsize=(10, 6))
    areas = ['LA Average', 'Venice', 'Santa Monica', 'Brentwood']
    premiums = [100, 115, 125, 140]
    
    bars = plt.bar(areas, premiums, color=['#95a5a6', '#FF6B6B', '#4ECDC4', '#45B7D1'])
    plt.axhline(y=100, color='black', linestyle='--', alpha=0.5)
    plt.title('Price Premium Index by Area (LA Average = 100)', fontsize=16, fontweight='bold')
    plt.ylabel('Price Index', fontsize=12)
    
    for bar, premium in zip(bars, premiums):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{premium}%', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    plt.show()

# Chart 6: Daily Traffic Patterns
def chart6_traffic_patterns():
    plt.figure(figsize=(12, 6))
    hours = list(range(6, 22))
    venice_traffic = [20, 35, 40, 30, 25, 30, 45, 50, 45, 35, 40, 60, 75, 70, 65, 50]
    sm_traffic = [30, 55, 70, 65, 50, 60, 75, 80, 70, 55, 65, 70, 65, 55, 45, 35]
    brentwood_traffic = [15, 25, 35, 55, 60, 65, 60, 55, 50, 65, 70, 65, 50, 40, 30, 20]
    
    plt.plot(hours, venice_traffic, 'o-', label='Venice', linewidth=2)
    plt.plot(hours, sm_traffic, 's-', label='Santa Monica', linewidth=2)
    plt.plot(hours, brentwood_traffic, '^-', label='Brentwood', linewidth=2)
    
    plt.title('Daily Foot Traffic Patterns by Neighborhood', fontsize=16, fontweight='bold')
    plt.xlabel('Hour of Day', fontsize=12)
    plt.ylabel('Relative Traffic (%)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(hours)
    plt.tight_layout()
    plt.show()

# Chart 7: Business Category Distribution
def chart7_business_categories():
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    
    # Santa Monica
    sm_categories = ['Tech/Creative', 'Health/Wellness', 'Hospitality', 'Retail', 'Services']
    sm_percentages = [32, 26, 12, 15, 15]
    ax1.pie(sm_percentages, labels=sm_categories, autopct='%1.1f%%', startangle=90)
    ax1.set_title('Santa Monica', fontsize=14, fontweight='bold')
    
    # Venice
    v_categories = ['Retail/Boutiques', 'Food/Beverage', 'Creative', 'Health', 'Services']
    v_percentages = [28, 25, 20, 15, 12]
    ax2.pie(v_percentages, labels=v_categories, autopct='%1.1f%%', startangle=90)
    ax2.set_title('Venice', fontsize=14, fontweight='bold')
    
    # Brentwood
    b_categories = ['Professional', 'Retail/Dining', 'Medical', 'Personal', 'Other']
    b_percentages = [35, 30, 20, 10, 5]
    ax3.pie(b_percentages, labels=b_categories, autopct='%1.1f%%', startangle=90)
    ax3.set_title('Brentwood', fontsize=14, fontweight='bold')
    
    plt.suptitle('Business Category Distribution by Neighborhood', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()

# Chart 8: Revenue by Commercial Corridor
def chart8_corridor_revenue():
    plt.figure(figsize=(12, 8))
    corridors = ['Ocean Ave', 'Main St', 'Abbot Kinney', 'Montana Ave', 'San Vicente', 'Country Mart']
    revenue = [450, 180, 120, 95, 85, 45]
    neighborhoods = ['SM', 'SM', 'Venice', 'SM', 'Brentwood', 'Brentwood']
    colors = ['#FF6B6B' if n == 'Venice' else '#4ECDC4' if n == 'SM' else '#45B7D1' for n in neighborhoods]
    
    bars = plt.barh(corridors, revenue, color=colors)
    plt.title('Annual Revenue by Commercial Corridor ($M)', fontsize=16, fontweight='bold')
    plt.xlabel('Revenue ($ Millions)', fontsize=12)
    
    for bar, rev in zip(bars, revenue):
        plt.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                f'${rev}M', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.show()

# Chart 9: Customer Education vs Price Tolerance
def chart9_education_price():
    plt.figure(figsize=(10, 8))
    education_rates = [49.3, 60, 70]
    price_premiums = [15, 25, 40]
    neighborhoods = ['Venice', 'Santa Monica', 'Brentwood']
    
    plt.scatter(education_rates, price_premiums, s=500, alpha=0.6, 
                c=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    
    for i, txt in enumerate(neighborhoods):
        plt.annotate(txt, (education_rates[i], price_premiums[i]), 
                    fontsize=12, ha='center', va='center')
    
    # Add trend line
    z = np.polyfit(education_rates, price_premiums, 1)
    p = np.poly1d(z)
    plt.plot(education_rates, p(education_rates), "r--", alpha=0.8)
    
    plt.title('Education Level vs Price Premium Tolerance', fontsize=16, fontweight='bold')
    plt.xlabel('College Graduation Rate (%)', fontsize=12)
    plt.ylabel('Price Premium Above LA Average (%)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# Chart 10: Peak Shopping Times Heatmap
def chart10_shopping_times():
    plt.figure(figsize=(12, 8))
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hours = ['6am', '8am', '10am', '12pm', '2pm', '4pm', '6pm', '8pm']
    
    # Shopping intensity (0-100)
    data = np.array([
        [10, 15, 12, 15, 20, 60, 40],  # 6am
        [30, 25, 28, 30, 35, 70, 65],  # 8am
        [50, 40, 45, 48, 55, 90, 85],  # 10am
        [70, 55, 65, 68, 75, 95, 90],  # 12pm
        [65, 50, 60, 62, 70, 85, 80],  # 2pm
        [45, 35, 40, 45, 60, 80, 70],  # 4pm
        [55, 45, 50, 55, 75, 85, 75],  # 6pm
        [40, 30, 35, 40, 65, 70, 60],  # 8pm
    ])
    
    sns.heatmap(data, annot=True, fmt='d', cmap='RdYlBu_r',
                xticklabels=days, yticklabels=hours,
                cbar_kws={'label': 'Shopping Intensity'})
    plt.title('Weekly Shopping Intensity Patterns (All Areas)', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()

# Chart 11: Business Survival Rates
def chart11_survival_rates():
    plt.figure(figsize=(10, 6))
    years = [1, 2, 3, 4, 5]
    venice_survival = [92, 85, 78, 72, 68]
    sm_survival = [94, 88, 82, 76, 71]
    brentwood_survival = [96, 92, 87, 82, 78]
    
    plt.plot(years, venice_survival, 'o-', label='Venice', linewidth=2, markersize=8)
    plt.plot(years, sm_survival, 's-', label='Santa Monica', linewidth=2, markersize=8)
    plt.plot(years, brentwood_survival, '^-', label='Brentwood', linewidth=2, markersize=8)
    
    plt.title('Business Survival Rates by Year', fontsize=16, fontweight='bold')
    plt.xlabel('Years in Business', fontsize=12)
    plt.ylabel('Survival Rate (%)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(60, 100)
    plt.tight_layout()
    plt.show()

# Chart 12: Average Transaction Value
def chart12_transaction_values():
    plt.figure(figsize=(12, 6))
    categories = ['Coffee', 'Casual Dining', 'Fine Dining', 'Retail Fashion', 'Wellness', 'Services']
    venice_values = [8, 35, 75, 95, 65, 85]
    sm_values = [12, 45, 95, 125, 85, 125]
    brentwood_values = [15, 65, 145, 275, 150, 185]
    
    x = np.arange(len(categories))
    width = 0.25
    
    plt.bar(x - width, venice_values, width, label='Venice', color='#FF6B6B')
    plt.bar(x, sm_values, width, label='Santa Monica', color='#4ECDC4')
    plt.bar(x + width, brentwood_values, width, label='Brentwood', color='#45B7D1')
    
    plt.title('Average Transaction Value by Category ($)', fontsize=16, fontweight='bold')
    plt.xlabel('Business Category', fontsize=12)
    plt.ylabel('Average Transaction ($)', fontsize=12)
    plt.xticks(x, categories, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.show()

# Chart 13: Market Opportunity Matrix
def chart13_opportunity_matrix():
    plt.figure(figsize=(10, 8))
    
    opportunities = ['Early Morning', 'Delivery', 'Experience Retail', 'Subscriptions', 
                    'Tuesday Events', 'Dog Services', 'Teen Market', 'Sustainability']
    demand_gap = [88, 68, 66, 34, 75, 45, 82, 71]  # % unmet demand
    difficulty = [20, 60, 70, 40, 25, 35, 55, 50]  # implementation difficulty
    
    colors = ['green' if d < 50 else 'orange' if d < 70 else 'red' for d in difficulty]
    
    plt.scatter(difficulty, demand_gap, s=500, alpha=0.6, c=colors)
    
    for i, txt in enumerate(opportunities):
        plt.annotate(txt, (difficulty[i], demand_gap[i]), 
                    fontsize=9, ha='center', va='center')
    
    plt.axhline(y=50, color='gray', linestyle='--', alpha=0.5)
    plt.axvline(x=50, color='gray', linestyle='--', alpha=0.5)
    
    plt.title('Market Opportunity Matrix', fontsize=16, fontweight='bold')
    plt.xlabel('Implementation Difficulty (0=Easy, 100=Hard)', fontsize=12)
    plt.ylabel('Unmet Demand (%)', fontsize=12)
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    
    # Add quadrant labels
    plt.text(25, 75, 'Quick Wins', fontsize=12, ha='center', alpha=0.7, fontweight='bold')
    plt.text(75, 75, 'Big Bets', fontsize=12, ha='center', alpha=0.7, fontweight='bold')
    plt.text(25, 25, 'Fill-ins', fontsize=12, ha='center', alpha=0.7, fontweight='bold')
    plt.text(75, 25, 'Question Marks', fontsize=12, ha='center', alpha=0.7, fontweight='bold')
    
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# Chart 14: Parking vs Revenue Correlation
def chart14_parking_revenue():
    plt.figure(figsize=(10, 8))
    
    businesses = ['Abbot Kinney', 'Main Street', 'Montana Ave', 'Ocean Ave', 
                  'San Vicente', 'Country Mart', 'Venice Boardwalk', 'Brentwood Village']
    parking_ratio = [0.8, 2.5, 3.5, 2.0, 4.5, 5.0, 0.3, 3.0]  # spaces per business
    revenue_per_sqft = [120, 95, 110, 150, 85, 90, 65, 105]
    
    plt.scatter(parking_ratio, revenue_per_sqft, s=400, alpha=0.6, 
                c=['#FF6B6B', '#4ECDC4', '#4ECDC4', '#4ECDC4', '#45B7D1', '#45B7D1', '#FF6B6B', '#45B7D1'])
    
    for i, txt in enumerate(businesses):
        plt.annotate(txt, (parking_ratio[i], revenue_per_sqft[i]), 
                    fontsize=9, ha='center', va='bottom', xytext=(0, 5), 
                    textcoords='offset points')
    
    plt.title('Parking Availability vs Revenue per Sq Ft', fontsize=16, fontweight='bold')
    plt.xlabel('Parking Spaces per Business', fontsize=12)
    plt.ylabel('Revenue per Sq Ft ($)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# Chart 15: Instagram Impact on Business
def chart15_instagram_impact():
    plt.figure(figsize=(12, 6))
    
    locations = ['Abbot Kinney', 'SM Pier', 'Venice Beach', 'Montana Ave', 
                 'Main Street', 'Country Mart', 'Ocean Ave', 'Rose Ave']
    instagram_posts = [2300000, 1800000, 1500000, 450000, 380000, 250000, 650000, 180000]
    revenue_boost = [45, 38, 42, 22, 25, 28, 32, 35]  # % revenue from Instagram-driven traffic
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()
    
    bars = ax1.bar(locations, [p/1000 for p in instagram_posts], alpha=0.7, color='#E1306C')
    line = ax2.plot(locations, revenue_boost, 'o-', color='#833AB4', linewidth=2, markersize=8)
    
    ax1.set_ylabel('Instagram Posts (Thousands)', fontsize=12)
    ax2.set_ylabel('Revenue from Instagram Traffic (%)', fontsize=12)
    ax1.set_title('Instagram Impact on Local Business', fontsize=16, fontweight='bold')
    ax1.set_xticklabels(locations, rotation=45, ha='right')
    
    plt.tight_layout()
    plt.show()

# Chart 16: Rent vs Revenue Efficiency
def chart16_rent_efficiency():
    plt.figure(figsize=(10, 8))
    
    business_types = ['Tech Office', 'Restaurant', 'Retail Boutique', 'Coffee Shop', 
                      'Wellness Studio', 'Gallery', 'Professional Service', 'Bar/Nightlife']
    rent_psf = [85, 75, 95, 65, 70, 60, 80, 90]
    revenue_psf = [320, 280, 180, 420, 250, 120, 380, 510]
    
    efficiency = [r/rent for r, rent in zip(revenue_psf, rent_psf)]
    colors = ['green' if e > 4 else 'yellow' if e > 3 else 'red' for e in efficiency]
    
    plt.scatter(rent_psf, revenue_psf, s=[e*100 for e in efficiency], alpha=0.6, c=colors)
    
    for i, txt in enumerate(business_types):
        plt.annotate(f'{txt}\n({efficiency[i]:.1f}x)', 
                    (rent_psf[i], revenue_psf[i]), 
                    fontsize=9, ha='center', va='center')
    
    # Add break-even line (3x rent)
    x_line = np.array([50, 100])
    plt.plot(x_line, x_line * 3, 'r--', alpha=0.5, label='3x Break-even')
    plt.plot(x_line, x_line * 4, 'g--', alpha=0.5, label='4x Healthy')
    
    plt.title('Rent vs Revenue Efficiency by Business Type', fontsize=16, fontweight='bold')
    plt.xlabel('Rent per Sq Ft ($)', fontsize=12)
    plt.ylabel('Revenue per Sq Ft ($)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# Chart 17: Seasonal Revenue Patterns
def chart17_seasonal_patterns():
    plt.figure(figsize=(12, 8))
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    venice_index = [85, 88, 95, 100, 105, 115, 130, 135, 110, 105, 95, 100]
    sm_index = [90, 92, 98, 102, 108, 112, 125, 128, 105, 102, 98, 105]
    brentwood_index = [95, 98, 102, 105, 100, 85, 80, 82, 115, 108, 105, 110]
    
    plt.plot(months, venice_index, 'o-', label='Venice', linewidth=2, markersize=8)
    plt.plot(months, sm_index, 's-', label='Santa Monica', linewidth=2, markersize=8)
    plt.plot(months, brentwood_index, '^-', label='Brentwood', linewidth=2, markersize=8)
    
    plt.axhline(y=100, color='gray', linestyle='--', alpha=0.5)
    plt.title('Seasonal Revenue Index by Neighborhood (100 = Average)', fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Revenue Index', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# Chart 18: Quick Decision Matrix - What to Sell Where
def chart18_decision_matrix():
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Products/Services
    products = ['Coffee/Cafe', 'Fast Casual Food', 'Fine Dining', 'Boutique Fashion', 
                'Wellness Services', 'Tech Services', 'Art/Creative', 'Professional Services',
                'Cannabis', 'Pet Services', 'Kids Activities', 'Nightlife/Bars']
    
    # Neighborhoods
    neighborhoods = ['Venice', 'Santa Monica', 'Brentwood']
    
    # Success scores (0-10)
    success_matrix = np.array([
        [9, 8, 6],   # Coffee/Cafe
        [8, 7, 5],   # Fast Casual
        [6, 8, 9],   # Fine Dining
        [7, 8, 9],   # Boutique Fashion
        [8, 9, 7],   # Wellness
        [5, 10, 6],  # Tech Services
        [10, 6, 4],  # Art/Creative
        [4, 7, 10],  # Professional Services
        [10, 6, 2],  # Cannabis
        [7, 8, 9],   # Pet Services
        [5, 7, 10],  # Kids Activities
        [9, 7, 3]    # Nightlife/Bars
    ])
    
    # Create heatmap
    im = ax.imshow(success_matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=10)
    
    # Set ticks
    ax.set_xticks(np.arange(len(neighborhoods)))
    ax.set_yticks(np.arange(len(products)))
    ax.set_xticklabels(neighborhoods)
    ax.set_yticklabels(products)
    
    # Rotate the tick labels
    plt.setp(ax.get_xticklabels(), rotation=0, ha="center")
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Success Potential (0-10)', rotation=270, labelpad=20)
    
    # Add text annotations
    for i in range(len(products)):
        for j in range(len(neighborhoods)):
            text = ax.text(j, i, success_matrix[i, j],
                          ha="center", va="center", color="white" if success_matrix[i, j] < 5 else "black",
                          fontweight='bold')
    
    ax.set_title('Quick Decision Matrix: What to Sell Where\n(10 = Highest Success Potential)', 
                 fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.show()

# Function to display all charts
def show_all_charts():
    """Display all 18 charts for quick business decision making"""
    print("Generating 18 Market Analysis Charts...\n")
    
    chart1_income_distribution()
    chart2_business_density()
    chart3_customer_archetypes()
    chart4_growth_sectors()
    chart5_price_premium()
    chart6_traffic_patterns()
    chart7_business_categories()
    chart8_corridor_revenue()
    chart9_education_price()
    chart10_shopping_times()
    chart11_survival_rates()
    chart12_transaction_values()
    chart13_opportunity_matrix()
    chart14_parking_revenue()
    chart15_instagram_impact()
    chart16_rent_efficiency()
    chart17_seasonal_patterns()
    chart18_decision_matrix()

# Run all charts if executed directly
if __name__ == "__main__":
    show_all_charts() 