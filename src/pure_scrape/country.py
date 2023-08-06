def standardize_country(country_text):
    # The input country_text may be None or empty, so we have to check it before proceeding
    if not country_text:
        return country_text

    us_states = [
        'Alabama', 'AL', 'Alaska', 'AK', 'Arizona', 'AZ', 'Arkansas', 'AR', 'California', 'CA', 'Colorado', 'CO',
        'Connecticut', 'CT', 'Delaware', 'DE', 'Florida', 'FL', 'Georgia', 'GA', 'Hawaii', 'HI', 'Idaho', 'ID',
        'Illinois', 'IL', 'Indiana', 'IN', 'Iowa', 'IA', 'Kansas', 'KS', 'Kentucky', 'KY', 'Louisiana', 'LA',
        'Maine', 'ME', 'Maryland', 'MD', 'Massachusetts', 'MA', 'Michigan', 'MI', 'Minnesota', 'MN', 'Mississippi', 'MS',
        'Missouri', 'MO', 'Montana', 'MT', 'Nebraska', 'NE', 'Nevada', 'NV', 'New Hampshire', 'NH', 'New Jersey', 'NJ',
        'New Mexico', 'NM', 'New York', 'NY', 'North Carolina', 'NC', 'North Dakota', 'ND', 'Ohio', 'OH', 'Oklahoma', 'OK',
        'Oregon', 'OR', 'Pennsylvania', 'PA', 'Rhode Island', 'RI', 'South Carolina', 'SC', 'South Dakota', 'SD',
        'Tennessee', 'TN', 'Texas', 'TX', 'Utah', 'UT', 'Vermont', 'VT', 'Virginia', 'VA', 'Washington', 'WA',
        'West Virginia', 'WV', 'Wisconsin', 'WI', 'Wyoming', 'WY'
    ]

    canadian_provinces_territories = [
        'Alberta', 'AB', 'British Columbia', 'BC', 'Manitoba', 'MB', 'New Brunswick', 'NB',
        'Newfoundland and Labrador', 'NL', 'Nova Scotia', 'NS', 'Ontario', 'ON', 'Prince Edward Island', 'PE',
        'Quebec', 'QC', 'Saskatchewan', 'SK', 'Northwest Territories', 'NT', 'Nunavut', 'NU', 'Yukon', 'YT'
    ]

    if 'United States' in country_text or any(state in country_text for state in us_states):
        return 'United States'

    elif 'Canada' in country_text or any(province in country_text for province in canadian_provinces_territories):
        return 'Canada'

    else:
        return None

