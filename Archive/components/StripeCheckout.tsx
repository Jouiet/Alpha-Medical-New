'use client';

import { useEffect, useState } from 'react';
import { Elements, PaymentElement, useStripe, useElements } from '@stripe/react-stripe-js';
import { getStripe } from '@/lib/stripe';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2 } from 'lucide-react';

interface CheckoutFormProps {
  amount: number;
  onSuccess: () => void;
  onError: (error: string) => void;
}

function CheckoutForm({ amount, onSuccess, onError }: CheckoutFormProps) {
  const stripe = useStripe();
  const elements = useElements();
  const [isProcessing, setIsProcessing] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!stripe || !elements) {
      return;
    }

    setIsProcessing(true);
    setErrorMessage('');

    try {
      const { error, paymentIntent } = await stripe.confirmPayment({
        elements,
        confirmParams: {
          return_url: `${window.location.origin}/checkout/success`,
        },
        redirect: 'if_required',
      });

      if (error) {
        setErrorMessage(error.message || 'Payment failed');
        onError(error.message || 'Payment failed');
      } else if (paymentIntent && paymentIntent.status === 'succeeded') {
        onSuccess();
      }
    } catch (err: any) {
      setErrorMessage(err.message || 'An unexpected error occurred');
      onError(err.message || 'An unexpected error occurred');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <PaymentElement />

      {errorMessage && (
        <Alert variant="destructive">
          <AlertDescription>{errorMessage}</AlertDescription>
        </Alert>
      )}

      <Button
        type="submit"
        className="w-full bg-blue-600 hover:bg-blue-700"
        size="lg"
        disabled={!stripe || isProcessing}
      >
        {isProcessing ? (
          <>
            <Loader2 className="mr-2 h-5 w-5 animate-spin" />
            Processing...
          </>
        ) : (
          `Pay $${amount.toFixed(2)}`
        )}
      </Button>
    </form>
  );
}

interface StripeCheckoutProps {
  amount: number;
  metadata?: Record<string, string>;
  onSuccess: () => void;
  onError: (error: string) => void;
}

export default function StripeCheckout({ amount, metadata, onSuccess, onError }: StripeCheckoutProps) {
  const [clientSecret, setClientSecret] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Create payment intent
    fetch('/api/create-payment-intent', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        amount,
        currency: 'usd',
        metadata,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.clientSecret) {
          setClientSecret(data.clientSecret);
        } else {
          onError('Failed to initialize payment');
        }
      })
      .catch((err) => {
        onError('Failed to initialize payment');
      })
      .finally(() => {
        setLoading(false);
      });
  }, [amount, metadata, onError]);

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
      </div>
    );
  }

  if (!clientSecret) {
    return (
      <Alert variant="destructive">
        <AlertDescription>Failed to load payment form. Please try again.</AlertDescription>
      </Alert>
    );
  }

  const stripePromise = getStripe();

  return (
    <Elements
      stripe={stripePromise}
      options={{
        clientSecret,
        appearance: {
          theme: 'stripe',
          variables: {
            colorPrimary: '#2563eb',
            colorBackground: '#ffffff',
            colorText: '#1e293b',
            colorDanger: '#dc2626',
            fontFamily: 'Inter, system-ui, sans-serif',
            borderRadius: '8px',
          },
        },
      }}
    >
      <CheckoutForm amount={amount} onSuccess={onSuccess} onError={onError} />
    </Elements>
  );
}
