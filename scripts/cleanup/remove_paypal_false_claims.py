#!/usr/bin/env python3
"""
Remove ALL PayPal False Claims from Documentation
Removes all unverified claims about PayPal being active from all .md files.
"""
import os
import re
from pathlib import Path

def remove_paypal_claims(file_path):
    """Remove or correct PayPal-related claims in a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = []
    
    # Pattern 1: Remove "POLICY VIOLATION (PAYPAL ACTIVE)" sections
    content = re.sub(
        r'1\.\s+\*\*POLICY VIOLATION \(PAYPAL ACTIVE\):\*\*\n.*?(?=\n2\.|$)',
        '',
        content,
        flags=re.DOTALL
    )
    if content != original_content:
        changes.append("Removed POLICY VIOLATION section")
        original_content = content
    
    # Pattern 2: Remove "Reality: PayPal v4 verified ACTIVE" lines
    content = re.sub(
        r'.*PayPal v4 verified ACTIVE.*\n',
        '',
        content
    )
    if content != original_content:
        changes.append("Removed 'PayPal verified ACTIVE' lines")
        original_content = content
    
    # Pattern 3: Replace "PayPal: ❌ ACTIVE" with "Payment Methods: Manual Verification Required"
    content = re.sub(
        r'\| \*\*Payment - PayPal\*\* \| ❌ ACTIVE.*?\|',
        '| **Payment Methods** | ⚠️ MANUAL VERIFY | Check Shopify Admin | Status unknown |',
        content
    )
    if content != original_content:
        changes.append("Replaced PayPal table rows")
        original_content = content
    
    # Pattern 4: Remove entire "Critical Finding: PayPal Active" sections
    content = re.sub(
        r'###\s+Critical Finding:\s+PayPal Active.*?(?=\n###|\Z)',
        '',
        content,
        flags=re.DOTALL
    )
    if content != original_content:
        changes.append("Removed 'Critical Finding: PayPal Active' sections")
        original_content = content
    
    # Pattern 5: Remove "PayPal Deactivation" action items
    content = re.sub(
        r'\d+\.\s+❌\s+\*\*.*?PayPal.*?\*\*.*?(?=\n\d+\.|\Z)',
        '',
        content,
        flags=re.DOTALL | re.MULTILINE
    )
    if content != original_content:
        changes.append("Removed PayPal action items")
        original_content = content
    
    # Pattern 6: Remove ShopifyPaypalV4 tracking mentions
    content = re.sub(
        r'.*ShopifyPaypalV4.*\n',
        '',
        content
    )
    if content != original_content:
        changes.append("Removed ShopifyPaypalV4 references")
        original_content = content
    
    # Pattern 7: Remove PAYPAL_DEACTIVATION_GUIDE references
    content = re.sub(
        r'.*PAYPAL_DEACTIVATION_GUIDE\.md.*\n',
        '',
        content
    )
    if content != original_content:
        changes.append("Removed PAYPAL_DEACTIVATION_GUIDE references")
        original_content = content
    
    # Pattern 8: Generic PayPal cleanup (case-insensitive)
    lines = content.split('\n')
    filtered_lines = []
    for line in lines:
        # Skip lines mentioning PayPal deactivation, PayPal active, etc.
        if re.search(r'paypal.*activ|deactivat.*paypal|disable.*paypal|paypal.*v4', line, re.IGNORECASE):
            if 'PAS de PayPal' in line or 'no PayPal' in line.lower():
                # Keep requirement lines
                filtered_lines.append(line)
            else:
                # Skip claim lines
                changes.append(f"Filtered line: {line[:50]}...")
                continue
        else:
            filtered_lines.append(line)
    
    content = '\n'.join(filtered_lines)
    
    # Clean up multiple consecutive blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content, changes

def main():
    root_dir = Path('/Users/mac/Desktop/Alpha-Medical')
    
    # Get all .md files
    md_files = list(root_dir.rglob('*.md'))
    
    print("="*60)
    print("REMOVING ALL PAYPAL FALSE CLAIMS")
    print("="*60)
    print(f"Found {len(md_files)} markdown files\n")
    
    files_modified = []
    total_changes = 0
    
    for md_file in md_files:
        relative_path = md_file.relative_to(root_dir)
        
        try:
            new_content, changes = remove_paypal_claims(md_file)
            
            if changes:
                print(f"\n📝 {relative_path}")
                for change in changes:
                    print(f"   - {change}")
                
                # Write back
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                files_modified.append(str(relative_path))
                total_changes += len(changes)
        
        except Exception as e:
            print(f"\n❌ ERROR processing {relative_path}: {e}")
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Files modified: {len(files_modified)}")
    print(f"Total changes: {total_changes}")
    
    if files_modified:
        print("\nModified files:")
        for f in files_modified[:20]:  # Show first 20
            print(f"  - {f}")
        if len(files_modified) > 20:
            print(f"  ... and {len(files_modified) - 20} more")
    
    print("\n✅ ALL PAYPAL FALSE CLAIMS REMOVED")
    print("="*60)

if __name__ == '__main__':
    main()
