'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import ButtonFilled from '@/components/ButtonFilled'

export default function MfaOtpPage() {
  const router = useRouter()
  const [qrCode, setQrCode] = useState<string | null>(null)
  const [otp, setOtp] = useState('')
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(true)

  
    useEffect(() => {
    const storedEmail = localStorage.getItem('userEmail')
    if (!storedEmail) return

    setEmail(storedEmail)

    const fetchQr = async () => {
        try {
        const res = await fetch('/api/auth/mfa/enable', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: storedEmail }),
        })

        const data = await res.json()
        if (res.ok && data.qr_code) {
            setQrCode(data.qr_code)
        }
        } catch (err) {
        console.error('Failed to fetch MFA QR:', err)
        }
    }

    fetchQr()
    }, [])


    const handleVerifyOtp = async () => {
    try {
        const res = await fetch('http://127.0.0.1:8000/auth/verify-otp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: email, otp }),
        })
        const data = await res.json()

        if (data.access_token) {
        // ✅ Store token
        localStorage.setItem('access_token', data.access_token)
        localStorage.removeItem('mfa_email')
        localStorage.removeItem('mfa_qr')
        window.location.href = '/' // redirect to dashboard/home
        } else {
        alert(data.message)
        }
    } catch (err) {
        alert('OTP verification failed')
        console.error(err)
    }finally {
        setLoading(false) // Stop loading (unless successful and redirecting)
    }
    }


  if (loading) return <p className="text-center p-4">Loading QR code...</p>

  return (
    <div className="flex flex-col items-center justify-center p-8">
      <p>Scan this QR code using your Authenticator App</p>
      <img src={`data:image/png;base64,${qrCode}`} alt="QR Code" className="my-4" />
      <input
        type="text"
        placeholder="Enter OTP"
        value={otp}
        onChange={(e) => setOtp(e.target.value)}
        className="border p-2 rounded mb-4 w-full max-w-xs text-center"
      />
      <ButtonFilled onClick={handleVerifyOtp} disabled={loading}>
  {loading ? 'Verifying...' : 'Verify OTP'}
</ButtonFilled>
    </div>
  )
}
