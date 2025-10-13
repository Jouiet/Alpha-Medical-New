'use client';

import { useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, Bell, Mail, Lock, Globe, Eye, Shield } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { toast } from 'sonner';

export default function SettingsPage() {
  const [settings, setSettings] = useState({
    emailNotifications: true,
    pushNotifications: false,
    orderUpdates: true,
    promotionalEmails: true,
    productRecommendations: true,
    twoFactorAuth: false,
    language: 'en',
    currency: 'USD',
    timezone: 'America/New_York',
  });

  const handleToggle = (key: keyof typeof settings) => {
    setSettings({
      ...settings,
      [key]: !settings[key],
    });
    toast.success('Settings updated');
  };

  const handleSelectChange = (key: keyof typeof settings, value: string) => {
    setSettings({
      ...settings,
      [key]: value,
    });
    toast.success('Settings updated');
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-6">
        <Link href="/account" className="inline-flex items-center text-blue-600 hover:text-blue-700">
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Account
        </Link>
      </div>

      <div className="mb-8">
        <h1 className="mb-2 text-3xl font-bold text-slate-900">Settings</h1>
        <p className="text-slate-600">Manage your account preferences</p>
      </div>

      <div className="space-y-6">
        {/* Notifications */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Bell className="h-5 w-5" />
              Notifications
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <Label htmlFor="emailNotifications" className="font-medium text-slate-900">
                  Email Notifications
                </Label>
                <p className="text-sm text-slate-600">Receive notifications via email</p>
              </div>
              <Switch
                id="emailNotifications"
                checked={settings.emailNotifications}
                onCheckedChange={() => handleToggle('emailNotifications')}
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <Label htmlFor="pushNotifications" className="font-medium text-slate-900">
                  Push Notifications
                </Label>
                <p className="text-sm text-slate-600">Receive browser push notifications</p>
              </div>
              <Switch
                id="pushNotifications"
                checked={settings.pushNotifications}
                onCheckedChange={() => handleToggle('pushNotifications')}
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <Label htmlFor="orderUpdates" className="font-medium text-slate-900">
                  Order Updates
                </Label>
                <p className="text-sm text-slate-600">Get notified about order status changes</p>
              </div>
              <Switch
                id="orderUpdates"
                checked={settings.orderUpdates}
                onCheckedChange={() => handleToggle('orderUpdates')}
              />
            </div>
          </CardContent>
        </Card>

        {/* Marketing */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Mail className="h-5 w-5" />
              Marketing Preferences
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <Label htmlFor="promotionalEmails" className="font-medium text-slate-900">
                  Promotional Emails
                </Label>
                <p className="text-sm text-slate-600">Receive emails about sales and offers</p>
              </div>
              <Switch
                id="promotionalEmails"
                checked={settings.promotionalEmails}
                onCheckedChange={() => handleToggle('promotionalEmails')}
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <Label htmlFor="productRecommendations" className="font-medium text-slate-900">
                  Product Recommendations
                </Label>
                <p className="text-sm text-slate-600">Get personalized product suggestions</p>
              </div>
              <Switch
                id="productRecommendations"
                checked={settings.productRecommendations}
                onCheckedChange={() => handleToggle('productRecommendations')}
              />
            </div>
          </CardContent>
        </Card>

        {/* Security */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Shield className="h-5 w-5" />
              Security
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <Label htmlFor="twoFactorAuth" className="font-medium text-slate-900">
                  Two-Factor Authentication
                </Label>
                <p className="text-sm text-slate-600">Add extra security to your account</p>
              </div>
              <Switch
                id="twoFactorAuth"
                checked={settings.twoFactorAuth}
                onCheckedChange={() => handleToggle('twoFactorAuth')}
              />
            </div>

            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium text-slate-900">Change Password</p>
                <p className="text-sm text-slate-600">Update your password regularly</p>
              </div>
              <Button variant="outline" size="sm">
                <Lock className="mr-2 h-4 w-4" />
                Change
              </Button>
            </div>

            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium text-slate-900">Active Sessions</p>
                <p className="text-sm text-slate-600">Manage logged-in devices</p>
              </div>
              <Button variant="outline" size="sm">
                <Eye className="mr-2 h-4 w-4" />
                View
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Preferences */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Globe className="h-5 w-5" />
              Regional Preferences
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <Label htmlFor="language" className="mb-2 block font-medium text-slate-900">
                Language
              </Label>
              <Select
                value={settings.language}
                onValueChange={(value) => handleSelectChange('language', value)}
              >
                <SelectTrigger id="language">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="en">English</SelectItem>
                  <SelectItem value="es">Español</SelectItem>
                  <SelectItem value="fr">Français</SelectItem>
                  <SelectItem value="de">Deutsch</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="currency" className="mb-2 block font-medium text-slate-900">
                Currency
              </Label>
              <Select
                value={settings.currency}
                onValueChange={(value) => handleSelectChange('currency', value)}
              >
                <SelectTrigger id="currency">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="USD">USD - US Dollar</SelectItem>
                  <SelectItem value="EUR">EUR - Euro</SelectItem>
                  <SelectItem value="GBP">GBP - British Pound</SelectItem>
                  <SelectItem value="CAD">CAD - Canadian Dollar</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="timezone" className="mb-2 block font-medium text-slate-900">
                Timezone
              </Label>
              <Select
                value={settings.timezone}
                onValueChange={(value) => handleSelectChange('timezone', value)}
              >
                <SelectTrigger id="timezone">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="America/New_York">Eastern Time (ET)</SelectItem>
                  <SelectItem value="America/Chicago">Central Time (CT)</SelectItem>
                  <SelectItem value="America/Denver">Mountain Time (MT)</SelectItem>
                  <SelectItem value="America/Los_Angeles">Pacific Time (PT)</SelectItem>
                  <SelectItem value="Europe/London">London (GMT)</SelectItem>
                  <SelectItem value="Europe/Paris">Paris (CET)</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </CardContent>
        </Card>

        {/* Privacy */}
        <Card>
          <CardHeader>
            <CardTitle>Privacy & Data</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Button variant="outline" className="w-full justify-start">
              Download My Data
            </Button>
            <Button variant="outline" className="w-full justify-start text-red-600 hover:text-red-700">
              Delete Account
            </Button>
            <p className="text-xs text-slate-600">
              Deleting your account is permanent and cannot be undone. All your data will be removed.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
