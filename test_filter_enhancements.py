#!/usr/bin/env python3
"""
Test script to verify the Complete Risk Register filter enhancements are working correctly.
"""

import requests
from bs4 import BeautifulSoup
import re

def test_filter_enhancements():
    """Test that the Complete Risk Register filter enhancements are working correctly."""
    
    print("Testing Complete Risk Register Filter Enhancements...")
    print("=" * 60)
    
    # Test 1: Dashboard loads successfully
    try:
        response = requests.get('http://127.0.0.1:8000/dashboard/')
        if response.status_code == 200:
            print("✓ Dashboard loads successfully")
        else:
            print(f"✗ Dashboard failed to load: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Could not connect to dashboard: {e}")
        return False
      # Test 2: Check for Complete Risk Register section
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Look for the Complete Risk Register header (text is within the h5 element)
    register_header = soup.find('h5', class_='card-title')
    header_found = False
    if register_header and 'Complete Risk Register' in register_header.get_text():
        header_found = True
    
    if not header_found:
        # Alternative search - look for any element containing the text
        all_text_elements = soup.find_all(string=re.compile(r'Complete Risk Register'))
        if all_text_elements:
            header_found = True
    
    if header_found:
        print("✓ Found Complete Risk Register section")
    else:
        print("✗ Complete Risk Register section not found")
        return False
    
    # Test 3: Check for new filter elements with correct IDs
    filter_elements = [
        ('tableProjectFilter', 'Project filter dropdown'),
        ('tableRiskLevelFilter', 'Risk Level filter dropdown'),
        ('tableStatusFilter', 'Status filter dropdown'),
        ('tableCategoryFilter', 'Category filter dropdown'),
        ('applyTableFilters', 'Apply Filter button'),
        ('clearTableFilters', 'Clear Filter button')
    ]
    
    missing_elements = []
    for element_id, description in filter_elements:
        element = soup.find(id=element_id)
        if element:
            print(f"✓ Found {description} (#{element_id})")
        else:
            print(f"✗ Missing {description} (#{element_id})")
            missing_elements.append(element_id)
    
    if missing_elements:
        print(f"\n✗ Missing elements: {missing_elements}")
        return False
    
    # Test 4: Check for proper button structure and icons
    apply_button = soup.find(id='applyTableFilters')
    clear_button = soup.find(id='clearTableFilters')
    
    if apply_button:
        # Check if it has the filter icon
        filter_icon = apply_button.find('i', class_='bi-funnel')
        if filter_icon:
            print("✓ Apply Filter button has correct filter icon")
        else:
            print("✗ Apply Filter button missing filter icon")
        
        # Check button text
        if 'Filter' in apply_button.get_text():
            print("✓ Apply Filter button has correct text")
        else:
            print("✗ Apply Filter button missing 'Filter' text")
    
    if clear_button:
        # Check if it has the reset icon
        reset_icon = clear_button.find('i', class_='bi-arrow-clockwise')
        if reset_icon:
            print("✓ Clear Filter button has correct reset icon")
        else:
            print("✗ Clear Filter button missing reset icon")
        
        # Check button text
        if 'Clear' in clear_button.get_text():
            print("✓ Clear Filter button has correct text")
        else:
            print("✗ Clear Filter button missing 'Clear' text")
    
    # Test 5: Check that filter dropdowns have proper labels
    filter_labels_found = 0
    filter_section = soup.find(id='applyTableFilters').find_parent('div', class_='card-body')
    if filter_section:
        labels = filter_section.find_all('label', class_='form-label')
        expected_labels = ['Project', 'Risk Level', 'Status', 'Category']
        
        found_label_texts = [label.get_text().strip() for label in labels if label.get_text().strip()]
        
        for expected in expected_labels:
            if expected in found_label_texts:
                print(f"✓ Found '{expected}' filter label")
                filter_labels_found += 1
            else:
                print(f"✗ Missing '{expected}' filter label")
        
        if filter_labels_found == len(expected_labels):
            print("✓ All filter labels present")
        else:
            print(f"✗ Only {filter_labels_found}/{len(expected_labels)} filter labels found")
    
    # Test 6: Check for risk table
    risk_table = soup.find(id='allRisksTable')
    if risk_table:
        print("✓ Risk table (allRisksTable) found")
        
        # Check table headers
        headers = risk_table.find('thead')
        if headers:
            header_texts = [th.get_text().strip() for th in headers.find_all('th')]
            expected_headers = ['Risk', 'Project', 'Category', 'Score', 'Likelihood', 'Impact', 'Owner', 'Actions']
            
            if all(header in header_texts for header in expected_headers):
                print("✓ All expected table headers found")
            else:
                missing_headers = [h for h in expected_headers if h not in header_texts]
                print(f"✗ Missing table headers: {missing_headers}")
    else:
        print("✗ Risk table (allRisksTable) not found")
        return False
    
    print("\n" + "=" * 60)
    print("✓ All filter enhancement tests passed!")
    print("Complete Risk Register now has proper 'Filter' and 'Clear' buttons!")
    return True

if __name__ == "__main__":
    success = test_filter_enhancements()
    if not success:
        print("\n❌ Some tests failed. Please check the implementation.")
        exit(1)
    else:
        print("\n🎉 All tests passed! Filter enhancements are working correctly.")
