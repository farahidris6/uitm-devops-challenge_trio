'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

export default function SetupMfaPage() {
  const [qrCode, setQrCode] = useState<string | null>(null)
  const [otp, setOtp] = useState('')
  const [email, setEmail] = useState('')
  const router = useRouter()

  useEffect(() => {
    // get email from localStorage/sessionStorage or pass via query param
    const storedEmail = localStorage.getItem('mfa_email')
    if (storedEmail) setEmail(storedEmail)

    const fetchQr = async () => {
      if (!storedEmail) return
      const res = await fetch('api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: storedEmail, password: 'dummy', mfa_type: 'app' })
      })
      const data = await res.json()
      if (data.qr_code) setQrCode(data.qr_code)
        return
    }
    
    fetchQr()
  }, [])

  const handleVerifyOtp = async () => {
    const res = await fetch('http://127.0.0.1:8000/auth/verify-otp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: email, otp })
    })
    const data = await res.json()
    if (data.message.includes('Login successful')) {
      alert('Login successful!')
      router.push('/') // redirect home
    } else {
      alert(data.message)
    }
  }

  if (!qrCode) return <div>Loading QR code...</div>

  return (
    <div className="flex flex-col items-center justify-center min-h-screen space-y-6">
      <h2 className="text-2xl font-semibold">Setup MFA</h2>
      <p>Scan this QR code with your Authenticator App:</p>
      <img src={`data:image/png;base64,${qrCode}`} alt="QR Code" />
      <input
        type="text"
        placeholder="Enter OTP"
        value={otp}
        onChange={(e) => setOtp(e.target.value)}
        className="border border-slate-300 rounded-lg p-2"
      />
      <button onClick={handleVerifyOtp} className="bg-blue-500 text-white p-2 rounded-lg">
        Verify OTP
      </button>
    </div>
  )
}
