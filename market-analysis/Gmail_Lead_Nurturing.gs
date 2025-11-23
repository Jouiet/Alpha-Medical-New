/**
 * GMAIL LEAD NURTURING AUTOMATION - Google Apps Script
 * Attach to Google Sheets: Alpha Medical - Lead Management
 *
 * What it does:
 *   1. Reads "Qualified Leads" sheet
 *   2. Sends personalized emails to leads with status = "New"
 *   3. Updates status to "Contacted" + timestamps
 *   4. Respects Gmail rate limits (100 emails/day free tier)
 *
 * Setup:
 *   1. Open your Google Sheet: "Alpha Medical - Lead Management"
 *   2. Extensions → Apps Script
 *   3. Delete default code, paste this entire file
 *   4. Save (name: Gmail_Lead_Nurturing)
 *   5. Run → authorize permissions
 *   6. Triggers → Add trigger → sendLeadEmails → Time-driven → Day timer → 10-11am
 *
 * Gmail Limits:
 *   - Free Gmail: 100 emails/day
 *   - Google Workspace: 2000 emails/day
 */

// =============================================================================
// CONFIGURATION
// =============================================================================

const CONFIG = {
  SHEET_NAME: 'Qualified Leads',
  FROM_NAME: 'Alpha Medical Team',
  RATE_LIMIT_SECONDS: 2,  // Wait 2 seconds between emails
  MAX_EMAILS_PER_RUN: 50, // Safety limit
  TEST_MODE: false         // Set to true to log without sending
};

// =============================================================================
// EMAIL TEMPLATES
// =============================================================================

function getEmailTemplate(persona, quality_score, lead_name) {
  const priority = quality_score >= 8.5 ? 'hot' : (quality_score >= 7.5 ? 'warm' : 'cold');

  // Base template data
  const templates = {
    seniors: {
      hot: {
        subject: 'Natural Relief for Joint Pain - Alpha Medical',
        html: `
          <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
              <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c5aa0;">Relief for Your Pain is Here</h2>

                <p>Hi ${lead_name || 'there'},</p>

                <p>Living with joint pain is exhausting. At <strong>Alpha Medical</strong>, we specialize in medical-grade pain relief products trusted by <strong>10,000+ customers across 33 countries</strong>.</p>

                <div style="background: #f8f9fa; padding: 15px; border-left: 4px solid #2c5aa0; margin: 20px 0;">
                  <p style="margin: 0;"><strong>🎁 Special Offer: 25% OFF your first order</strong></p>
                  <p style="margin: 10px 0 0 0;">Use code: <code style="background: #fff; padding: 5px 10px; border-radius: 3px;">WELCOME25</code></p>
                </div>

                <p><strong>Our most popular pain relief products:</strong></p>
                <ul>
                  <li>Tourmaline Self-Heating Knee Pads</li>
                  <li>Magnetic Therapy Back Support Belt</li>
                  <li>Compression Therapy Ankle Sleeves</li>
                </ul>

                <p style="text-align: center; margin: 30px 0;">
                  <a href="https://alphamedical.shop/collections/pain-relief" style="background: #2c5aa0; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">Shop Pain Relief →</a>
                </p>

                <p>✓ Free shipping worldwide<br>
                ✓ 30-day money-back guarantee<br>
                ✓ Medical-grade quality</p>

                <p>Questions? Just reply to this email.</p>

                <p>Best,<br>
                <strong>Alpha Medical Team</strong><br>
                <a href="https://alphamedical.shop">alphamedical.shop</a></p>

                <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
                <p style="font-size: 12px; color: #666;">You received this email because you showed interest in pain relief solutions.</p>
              </div>
            </body>
          </html>
        `
      },
      warm: {
        subject: '3 Ways to Manage Joint Pain Naturally',
        html: `
          <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
              <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c5aa0;">3 Ways to Manage Joint Pain Naturally</h2>

                <p>Hi ${lead_name || 'there'},</p>

                <p>Living with pain is exhausting. Here are 3 natural approaches that can help:</p>

                <div style="background: #f8f9fa; padding: 15px; margin: 20px 0;">
                  <h3 style="color: #2c5aa0; margin-top: 0;">1. Medical-Grade Compression Support</h3>
                  <p>Targeted compression improves circulation and reduces inflammation.</p>

                  <h3 style="color: #2c5aa0;">2. Magnetic Therapy</h3>
                  <p>Natural magnetic fields can help reduce pain and improve joint mobility.</p>

                  <h3 style="color: #2c5aa0;">3. Ergonomic Posture Aids</h3>
                  <p>Proper support prevents strain and reduces chronic pain.</p>
                </div>

                <p>At <strong>Alpha Medical</strong>, we offer all three solutions - trusted by 10,000+ customers worldwide.</p>

                <p style="text-align: center; margin: 30px 0;">
                  <a href="https://alphamedical.shop/collections/all" style="background: #2c5aa0; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">Browse Solutions →</a>
                </p>

                <p>Questions? Just reply.</p>

                <p>Best,<br>
                <strong>Alpha Medical Team</strong></p>
              </div>
            </body>
          </html>
        `
      },
      cold: {
        subject: 'Understanding Your Pain Relief Options',
        html: `
          <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
              <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c5aa0;">Understanding Your Pain Relief Options</h2>

                <p>Hi ${lead_name || 'there'},</p>

                <p>If you're dealing with chronic pain, you're not alone. Millions of people worldwide seek natural, non-invasive relief.</p>

                <p><strong>Alpha Medical</strong> specializes in medical-grade pain relief products that work naturally with your body:</p>

                <ul>
                  <li>No prescription needed</li>
                  <li>Drug-free pain relief</li>
                  <li>Clinically tested materials</li>
                  <li>Trusted by 10,000+ customers</li>
                </ul>

                <p style="text-align: center; margin: 30px 0;">
                  <a href="https://alphamedical.shop" style="background: #2c5aa0; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">Learn More →</a>
                </p>

                <p>Best,<br>
                <strong>Alpha Medical Team</strong></p>
              </div>
            </body>
          </html>
        `
      }
    }
  };

  // Get template (default to seniors/cold if not found)
  const personaTemplates = templates[persona] || templates['seniors'];
  const template = personaTemplates[priority] || personaTemplates['cold'];

  return template;
}

// =============================================================================
// MAIN FUNCTION
// =============================================================================

function sendLeadEmails() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_NAME);

  if (!sheet) {
    Logger.log(`❌ ERROR: Sheet "${CONFIG.SHEET_NAME}" not found`);
    return;
  }

  const data = sheet.getDataRange().getValues();
  const headers = data[0];

  // Find column indices
  const colIndices = {
    contact: headers.indexOf('contact'),
    status: headers.indexOf('status'),
    persona: headers.indexOf('persona_match'),
    quality_score: headers.indexOf('quality_score'),
    name: headers.indexOf('name'),
    first_contact: headers.indexOf('first_contact_date'),
    last_contact: headers.indexOf('last_contact_date')
  };

  // Verify all columns exist
  for (const [col, idx] of Object.entries(colIndices)) {
    if (idx === -1) {
      Logger.log(`❌ ERROR: Column "${col}" not found in sheet`);
      return;
    }
  }

  let emailsSent = 0;
  let errors = 0;

  Logger.log(`========================================`);
  Logger.log(`GMAIL LEAD NURTURING - ${new Date()}`);
  Logger.log(`========================================`);

  // Skip header row
  for (let i = 1; i < data.length; i++) {
    const row = data[i];

    const contact = row[colIndices.contact];
    const status = row[colIndices.status];
    const persona = row[colIndices.persona];
    const quality_score = parseFloat(row[colIndices.quality_score]) || 0;
    const name = row[colIndices.name];

    // Only send to "New" leads with valid email
    if (status === 'New' && contact && contact.includes('@')) {

      // Safety limit
      if (emailsSent >= CONFIG.MAX_EMAILS_PER_RUN) {
        Logger.log(`⚠️  Reached max emails per run (${CONFIG.MAX_EMAILS_PER_RUN})`);
        break;
      }

      try {
        // Get email template
        const template = getEmailTemplate(persona, quality_score, name);

        if (CONFIG.TEST_MODE) {
          // Test mode: just log
          Logger.log(`[TEST] Would send to: ${contact} (${persona}, score: ${quality_score})`);
        } else {
          // Send email
          GmailApp.sendEmail(
            contact,
            template.subject,
            'Please view this email in an HTML-capable email client.',
            {
              htmlBody: template.html,
              name: CONFIG.FROM_NAME
            }
          );

          // Update status in sheet
          sheet.getRange(i + 1, colIndices.status + 1).setValue('Contacted');
          sheet.getRange(i + 1, colIndices.first_contact + 1).setValue(new Date());
          sheet.getRange(i + 1, colIndices.last_contact + 1).setValue(new Date());

          emailsSent++;
          Logger.log(`[${emailsSent}] ✅ Sent to: ${contact} (${persona}, score: ${quality_score})`);

          // Rate limit: Wait 2 seconds between emails
          Utilities.sleep(CONFIG.RATE_LIMIT_SECONDS * 1000);
        }

      } catch (e) {
        errors++;
        Logger.log(`[ERROR] Failed to send to ${contact}: ${e.message}`);
      }
    }
  }

  Logger.log(`========================================`);
  Logger.log(`SUMMARY`);
  Logger.log(`========================================`);
  Logger.log(`✅ Emails sent: ${emailsSent}`);
  Logger.log(`❌ Errors: ${errors}`);
  Logger.log(`⏰ Completed: ${new Date()}`);

  // Return summary (useful for testing)
  return {
    sent: emailsSent,
    errors: errors,
    timestamp: new Date()
  };
}

// =============================================================================
// UTILITY FUNCTIONS
// =============================================================================

/**
 * Test function - sends email to yourself for testing
 * Run this first before setting up automated trigger
 */
function testEmail() {
  const testEmail = Session.getActiveUser().getEmail();

  Logger.log(`Testing email to: ${testEmail}`);

  const template = getEmailTemplate('seniors', 8.5, 'Test User');

  GmailApp.sendEmail(
    testEmail,
    template.subject,
    'Please view this email in an HTML-capable email client.',
    {
      htmlBody: template.html,
      name: CONFIG.FROM_NAME
    }
  );

  Logger.log('✅ Test email sent! Check your inbox.');
}

/**
 * Check Gmail quota remaining
 */
function checkGmailQuota() {
  const quota = MailApp.getRemainingDailyQuota();
  Logger.log(`Gmail quota remaining today: ${quota} emails`);
  return quota;
}
