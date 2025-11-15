
# SHOPIFY FLOW - BUNDLE AUTO-CREATION NOTIFICATIONS

## WORKFLOW SETUP (Shopify Admin)

### Access Shopify Flow:
1. Admin → Settings → Apps and sales channels
2. Find "Shopify Flow" → Open app
3. Click "Create workflow"

### Configure Workflow:

**Name**: Bundle Auto-Creation Notifications

**Trigger**: Product created
- Condition: Product tags contains "auto-created"

**Action**: Send email to multiple recipients
- **Get data source**: Product metafield
  - Namespace: `auto_bundle`
  - Key: `customer_emails`
  - Type: JSON

- **Loop through emails**: For each email in customer_emails array

  **Send email**:
  - **To**: {{email}} (from loop)
  - **From**: noreply@alphamedical.shop
  - **Subject**: 🎉 Your Custom Bundle is Ready - 35% OFF!

  **Body** (HTML):
  ```html
  <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <div style="background: linear-gradient(135deg, #4A90E2 0%, #7FCCC9 100%); padding: 30px; text-align: center;">
      <h1 style="color: white; margin: 0;">🎉 Your Bundle is Ready!</h1>
    </div>

    <div style="padding: 40px 30px; background: #f9f9f9;">
      <p style="font-size: 16px; line-height: 1.6;">Hi there,</p>

      <p style="font-size: 16px; line-height: 1.6;">
        Great news! Your custom bundle proposal has been <strong>automatically created</strong>.
      </p>

      <p style="font-size: 16px; line-height: 1.6;">
        You and <strong>9+ other customers</strong> requested this exact combination,
        so we've made it official!
      </p>

      <div style="background: white; padding: 30px; border-radius: 12px; margin: 30px 0; text-align: center;">
        <h2 style="margin: 0 0 10px 0;">{{product.title}}</h2>
        <div style="margin: 20px 0;">
          <span style="text-decoration: line-through; color: #999; font-size: 18px;">
            ${{product.compare_at_price}}
          </span>
          <span style="font-size: 32px; font-weight: 700; color: #4A90E2; margin: 0 10px;">
            ${{product.price}}
          </span>
          <span style="background: #FF6B6B; color: white; padding: 6px 16px; border-radius: 20px; font-weight: 700;">
            35% OFF
          </span>
        </div>
        <a href="https://www.alphamedical.shop/products/{{product.handle}}"
           style="display: inline-block; margin-top: 20px; padding: 14px 32px; background: linear-gradient(135deg, #4A90E2 0%, #7FCCC9 100%); color: white; text-decoration: none; border-radius: 8px; font-weight: 600;">
          Shop This Bundle →
        </a>
      </div>

      <p style="font-size: 14px; color: #666; line-height: 1.6;">
        Thank you for being part of our community-driven product creation!
        Your feedback helps us create bundles that truly serve our customers.
      </p>

      <p style="font-size: 14px; color: #666;">
        Best regards,<br>
        <strong>Alpha Medical Team</strong>
      </p>
    </div>

    <div style="padding: 20px; text-align: center; background: #f0f0f0; font-size: 12px; color: #999;">
      <p>Alpha Medical | Professional Medical Equipment</p>
    </div>
  </div>
  ```

**Save workflow** and activate.

---

## TESTING FLOW

1. Manually create a test product with tag "auto-created"
2. Add metafield:
   - Namespace: `auto_bundle`
   - Key: `customer_emails`
   - Value: `["test@example.com"]`
3. Verify email is sent
4. Delete test product

---

## MONITORING

**Flow logs**:
- Admin → Settings → Apps → Shopify Flow → Workflows
- Click on workflow → View runs
- Check success/failures

**Email delivery**:
- Check Flow run logs for email delivery status
- Test with your own email first

---

STATUS: ✅ READY TO CONFIGURE
