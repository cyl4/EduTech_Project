// Login.jsx
import { useState, useEffect } from 'react'
import React from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button"

const Login = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();


  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setMessage('')
    setLoading(true)
    try {
      // Hook this to your Node backend
      // const res = await fetch('/api/auth/login', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ email, password, remember })
      // })
      // if (!res.ok) throw new Error('Invalid credentials')
      // const data = await res.json()
      // // Persist token if remember is true
      // if (remember) localStorage.setItem('token', data.token)
      // else sessionStorage.setItem('token', data.token)
      setMessage('Success! Redirecting…')
      // navigate('/dashboard') // if using react-router
    } catch (err) {
      setError(err.message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  const handleLogin = (e) => {
  e.preventDefault(); // Prevent page reload

  navigate('/Dashboard');
};

  return (
    <div className="flex min-h-svh flex-col items-center justify-center bg-gradient-to-b from-background to-muted/30 p-6">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="mb-6 text-center">
          <h1 className="text-2xl font-semibold tracking-tight md:text-3xl">Welcome back</h1>
          <p className="text-sm text-muted-foreground">Sign in to Presentation Prep Assistant</p>
        </div>

        {/* Card */}
        <div className="rounded-2xl border bg-card shadow-sm">
          <form onSubmit={handleSubmit} className="space-y-5 p-6">
            {/* Email */}
            <div className="space-y-2">
              <label htmlFor="email" className="text-sm font-medium">Email</label>
              <input
                id="email"
                type="email"
                placeholder="you@example.com"
                required
                className="w-full rounded-xl border bg-background px-3 py-2 outline-none transition focus:border-primary"
              />
            </div>

            {/* Password */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <label htmlFor="password" className="text-sm font-medium">Password</label>
                <a href="/forgot-password" className="text-xs text-primary hover:underline">Forgot?</a>
              </div>
              <input
                id="password"
                type="password"
                placeholder="••••••••"
                required
                className="w-full rounded-xl border bg-background px-3 py-2 outline-none transition focus:border-primary"
              />
            </div>

            {/* Remember me */}
            <div className="flex items-center justify-between">
              <label className="inline-flex cursor-pointer items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  onChange={(e) => setRemember(e.target.checked)}
                  className="h-4 w-4 rounded border"
                />
                Remember me
              </label>
              <a href="/signup" className="text-xs text-muted-foreground hover:text-foreground hover:underline">
                Create account
              </a>
            </div>

            {/* Error / Message */}
            {error && (
              <div className="rounded-xl border border-destructive/40 bg-destructive/10 p-3 text-sm text-destructive">
                {error}
              </div>
            )}
            {message && (
              <div className="rounded-xl border border-emerald-400/40 bg-emerald-400/10 p-3 text-sm text-emerald-600">
                {message}
              </div>
            )}

            {/* Submit */}
            <Button type="submit" onClick={handleLogin} className="w-full">
              Sign In
            </Button>
            

            {/* Divider */}
            <div className="relative py-2 text-center">
              <span className="px-2 text-xs uppercase tracking-wide text-muted-foreground">or continue with</span>
            </div>

            {/* Social placeholders */}
            <div className="grid grid-cols-3 gap-3">
              <Button variant="secondary" type="button" className="w-full">Google</Button>
              <Button variant="secondary" type="button" className="w-full">GitHub</Button>
              <Button variant="secondary" type="button" className="w-full">Microsoft</Button>
            </div>
          </form>
        </div>

        {/* Footer */}
        <p className="mt-6 text-center text-xs text-muted-foreground">
          By continuing you agree to our <a href="/terms" className="underline">Terms</a> and <a href="/privacy" className="underline">Privacy Policy</a>.
        </p>
      </div>

      {/* Keep a simple button to match your original structure (optional) */}
    </div>
  )
}

export default Login