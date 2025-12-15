import express from 'express'
import { monitorLogin } from '../middleware/loginMonitor.js'

const router = express.Router()

router.post('/login', monitorLogin, (req, res) => {
  const { email, password } = req.body

  // TEMP login simulation
  if (email === 'test@example.com' && password === 'Password123') {
    return res.status(200).json({ success: true, message: 'Login successful' })
  }

  return res.status(401).json({ success: false, message: 'Invalid credentials' })
})

export default router
