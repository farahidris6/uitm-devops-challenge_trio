import fs from 'fs'
import path from 'path'

const logFile = path.join(process.cwd(), 'src/logs/security.log')

export function logSecurityEvent(event) {
  const log = {
    ...event,
    timestamp: new Date().toISOString(),
  }

  fs.appendFileSync(logFile, JSON.stringify(log) + '\n')
}
