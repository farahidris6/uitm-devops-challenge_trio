import { logSecurityEvent } from '../services/securityLogger.js'

const failedAttempts = new Map()

export function monitorLogin(req, res, next) {
  const { email, username } = req.body
  const userKey = email || username || 'unknown'

  res.on('finish', () => {
    if (res.statusCode === 401 || res.statusCode === 400) {
      const attempts = failedAttempts.get(userKey) || 0
      failedAttempts.set(userKey, attempts + 1)

      logSecurityEvent({
        type: 'LOGIN_FAILED',
        user: userKey,
        attempts: attempts + 1,
        ip: req.ip,
      })

      // 🚨 Suspicious behavior
      if (attempts + 1 >= 3) {
        console.warn(`🚨 ALERT: Suspicious login detected for ${userKey}`)

        logSecurityEvent({
          type: 'SUSPICIOUS_LOGIN',
          user: userKey,
          reason: 'Multiple failed login attempts',
          ip: req.ip,
        })
      }
    }

    if (res.statusCode === 200) {
      failedAttempts.delete(userKey)

      logSecurityEvent({
        type: 'LOGIN_SUCCESS',
        user: userKey,
        ip: req.ip,
      })
    }
  })

  next()
}
