#!/usr/bin/env python3
"""
RESTORE country/language selector in footer__localization div
Replace empty div with proper render calls to localization snippets
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv('.env.admin')

SHOP_DOMAIN = os.getenv('SHOPIFY_STORE_DOMAIN')
ACCESS_TOKEN = os.getenv('SHOPIFY_ADMIN_ACCESS_TOKEN')
API_VERSION = '2025-10'
theme_id = 140069830733

def get_footer():
    url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/themes/{theme_id}/assets.json"
    headers = {'X-Shopify-Access-Token': ACCESS_TOKEN}
    response = requests.get(url, headers=headers, params={'asset[key]': 'sections/footer.liquid'})
    return response.json()['asset']['value']

def update_footer(content):
    url = f"https://{SHOP_DOMAIN}/admin/api/{API_VERSION}/themes/{theme_id}/assets.json"
    headers = {'X-Shopify-Access-Token': ACCESS_TOKEN}
    data = {'asset': {'key': 'sections/footer.liquid', 'value': content}}
    response = requests.put(url, headers=headers, json=data)
    return response.status_code == 200

# Get footer
footer = get_footer()

print("Finding empty footer__localization div to restore...")

# Find the empty localization div
# Current state (lines 286-288):
#   <div class="footer__column footer__localization isolate">
#   </div>
# </div>

# Target: Replace with proper structure
proper_structure = '''        <div class="footer__column footer__localization isolate">
          {%- if section.settings.enable_country_selector and localization.available_countries.size > 1 -%}
            <noscript>
              {%- form 'localization', id: 'FooterCountryFormNoScript', class: 'localization-form' -%}
                <div class="localization-form__select">
                  <h2 class="visually-hidden" id="FooterCountryLabelNoScript">{{ 'localization.country_label' | t }}</h2>
                  <select
                    class="localization-selector link"
                    name="country_code"
                    aria-labelledby="FooterCountryLabelNoScript"
                  >
                    {%- for country in localization.available_countries -%}
                      <option
                        value="{{ country.iso_code }}"
                        {%- if country.iso_code == localization.country.iso_code %}
                          selected
                        {% endif %}
                      >
                        {{ country.name }} ({{ country.currency.iso_code }}
                        {{ country.currency.symbol }})
                      </option>
                    {%- endfor -%}
                  </select>
                  {{ 'icon-caret.svg' | inline_asset_content }}
                </div>
                <button class="button button--tertiary">{{ 'localization.update_country' | t }}</button>
              {%- endform -%}
            </noscript>
            <localization-form>
              {%- form 'localization', id: 'FooterCountryForm', class: 'localization-form' -%}
                <div class="no-js-hidden">
                  <h2 class="caption-large text-body" id="FooterCountryLabel">
                    {{ 'localization.country_label' | t }}
                  </h2>
                  {%- render 'country-localization', localPosition: 'FooterCountry' -%}
                </div>
              {%- endform -%}
            </localization-form>
          {%- endif -%}

          {%- if section.settings.enable_language_selector and localization.available_languages.size > 1 -%}
            <noscript>
              {%- form 'localization', id: 'FooterLanguageFormNoScript', class: 'localization-form' -%}
                <div class="localization-form__select">
                  <h2 class="visually-hidden" id="FooterLanguageLabelNoScript">
                    {{ 'localization.language_label' | t }}
                  </h2>
                  <select
                    class="localization-selector link"
                    name="locale_code"
                    aria-labelledby="FooterLanguageLabelNoScript"
                  >
                    {%- for language in localization.available_languages -%}
                      <option
                        value="{{ language.iso_code }}"
                        lang="{{ language.iso_code }}"
                        {%- if language.iso_code == localization.language.iso_code %}
                          selected
                        {% endif %}
                      >
                        {{ language.endonym_name | capitalize }}
                      </option>
                    {%- endfor -%}
                  </select>
                  {{ 'icon-caret.svg' | inline_asset_content }}
                </div>
                <button class="button button--tertiary">{{ 'localization.update_language' | t }}</button>
              {%- endform -%}
            </noscript>

            <localization-form>
              {%- form 'localization', id: 'FooterLanguageForm', class: 'localization-form' -%}
                <div class="no-js-hidden">
                  <h2 class="caption-large text-body" id="FooterLanguageLabel">
                    {{ 'localization.language_label' | t }}
                  </h2>
                  {%- render 'language-localization', localPosition: 'FooterLanguage' -%}
                </div>
              {%- endform -%}
            </localization-form>
          {%- endif -%}
        </div>'''

# Find and replace the empty localization div
lines = footer.split('\n')

for i in range(len(lines) - 2):
    if ('footer__localization' in lines[i] and
        lines[i+1].strip() == '</div>' and
        lines[i+2].strip() == '</div>'):

        print(f"\n✅ Found empty localization div at lines {i+1}-{i+3}")
        print(f"   Current:")
        print(f"     {i+1}: {lines[i]}")
        print(f"     {i+2}: {lines[i+1]}")
        print(f"     {i+3}: {lines[i+2]}")

        # Replace the 3 empty lines with proper structure
        new_lines = lines[:i] + [proper_structure] + lines[i+3:]
        footer = '\n'.join(new_lines)

        print(f"\n✅ Replaced with proper country/language selector code")
        print(f"   Added:")
        print(f"     - Country selector (if enabled + multiple countries available)")
        print(f"     - Language selector (if enabled + multiple languages available)")
        print(f"     - Noscript fallbacks for both")
        print(f"     - Render calls to country-localization.liquid and language-localization.liquid")

        # Save for inspection
        with open('/tmp/footer_localization_restored.liquid', 'w') as f:
            f.write(footer)

        # Update Shopify
        print("\nUpdating Shopify...")
        if update_footer(footer):
            print("\n" + "="*70)
            print("✅ COUNTRY/LANGUAGE SELECTOR RESTORED")
            print("="*70)
            print("\nRestored:")
            print("  ✅ Country selector (United States | USD $)")
            print("  ✅ Language selector (if multiple languages)")
            print("  ✅ Proper footer__localization structure")
            print("\nResult:")
            print("  ✅ Footer bottom should now show Country/region selector")
            print("  ✅ Controlled by theme settings (enable_country_selector)")
            print("\nVerify: https://alphamedical.shop")
            print("Look for 'Country/region' at footer bottom")
        else:
            print("\n❌ Failed to update Shopify")

        break
else:
    print("\n❌ Empty localization div not found")
    print("Checking current state...")
    for i in range(280, min(295, len(lines))):
        print(f"{i+1:4d}: {lines[i]}")
