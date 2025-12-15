import express from 'express'
import authRoutes from './routes/auth.routes.js'

const app = express()

app.use(express.json())
app.use('/api/auth', authRoutes)

app.listen(4000, () => {
  console.log('🚀 Backend running on http://localhost:4000')
})
