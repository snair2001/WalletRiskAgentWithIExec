'use client'

import { useEffect, useState } from 'react'
import SeverityBadge from './SeverityBadge'

interface RiskData {
  currentScore: number
  confidence: number
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'
  timestamp: number
}

interface PortfolioData {
  totalValue: number
  walletAge: number
  transactions: number
  lastActivity: string
}

interface RiskDashboardProps {
  walletAddress: string
}

export default function RiskDashboard({ walletAddress }: RiskDashboardProps) {
  const [riskData, setRiskData] = useState<RiskData | null>(null)
  const [portfolioData, setPortfolioData] = useState<PortfolioData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true)
        setError(null)

        // Fetch portfolio data from API
        const portfolioResponse = await fetch(`/api/portfolio/${walletAddress}`)
        if (!portfolioResponse.ok) {
          throw new Error('Failed to fetch portfolio data')
        }
        const portfolio = await portfolioResponse.json()
        setPortfolioData(portfolio)

        // Call Python AI Agent
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
        const aiResponse = await fetch(`${apiUrl}/analyze`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            walletAddress,
            portfolio: portfolio
          })
        })

        if (!aiResponse.ok) {
           throw new Error('AI Agent unreachable (Ensure api_server.py is running)')
        }

        const aiResult = await aiResponse.json()

        // Map AI result to RiskData
        // Decision mapping: NO_ACTION->LOW, MONITOR->MEDIUM, etc.
        let severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL' = 'LOW'
        if (aiResult.decision === 'monitor') severity = 'MEDIUM' // Case sensitivity check?
        if (aiResult.decision === 'MONITOR') severity = 'MEDIUM'
        if (aiResult.decision === 'REQUEST_SEVERITY_ANALYSIS') severity = 'HIGH'
        if (aiResult.decision === 'ENFORCE_ACTION') severity = 'CRITICAL'

        setRiskData({
          currentScore: aiResult.risk_score,
          confidence: aiResult.confidence,
          severity: severity,
          timestamp: aiResult.timestamp * 1000
        })
      } catch (err) {
        console.error('Error fetching dashboard data:', err)
        setError(err instanceof Error ? err.message : 'Failed to load data')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [walletAddress])

  if (loading) {
    return (
      <div className="loading-spinner">
        <div className="spinner"></div>
        <p style={{ marginTop: '16px', color: 'var(--text-secondary)' }}>
          Loading portfolio data...
        </p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="glass-card" style={{ textAlign: 'center', padding: '40px' }}>
        <h3 style={{ color: 'var(--risk-high)', marginBottom: '12px' }}>⚠️ Error</h3>
        <p style={{ color: 'var(--text-secondary)' }}>{error}</p>
        <button 
          onClick={() => window.location.reload()}
          style={{
            marginTop: '16px',
            padding: '10px 20px',
            background: 'var(--primary)',
            border: 'none',
            borderRadius: '8px',
            color: 'white',
            cursor: 'pointer'
          }}
        >
          Retry
        </button>
      </div>
    )
  }

  if (!riskData || !portfolioData) return null

  return (
    <div className="risk-dashboard">
      {/* Main Risk Score Display */}
      <div className="risk-score-card glass-card">
        <h2>Current Risk Score</h2>
        <div className="score-display">
          <div className="score-value">
            {riskData.currentScore}
            <span className="score-max">/100</span>
          </div>
        </div>
        <SeverityBadge severity={riskData.severity} />
        <p className="confidence">
          Confidence: {riskData.confidence}%
        </p>
      </div>

      {/* Portfolio Info - NOW WITH REAL DATA */}
      <div className="glass-card">
        <h3 style={{ fontSize: '18px', marginBottom: '16px' }}>Portfolio Overview</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: 'var(--text-secondary)' }}>Total Value</span>
            <span style={{ fontWeight: '600' }}>${portfolioData.totalValue.toLocaleString()}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: 'var(--text-secondary)' }}>Wallet Age</span>
            <span style={{ fontWeight: '600' }}>
              {portfolioData.walletAge === 0 ? 'New wallet' : `${portfolioData.walletAge} days`}
            </span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: 'var(--text-secondary)' }}>Transactions</span>
            <span style={{ fontWeight: '600' }}>{portfolioData.transactions.toLocaleString()}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span style={{ color: 'var(--text-secondary)' }}>Last Activity</span>
            <span style={{ fontWeight: '600' }}>{portfolioData.lastActivity}</span>
          </div>
        </div>
      </div>

      {/* Risk Factors */}
      <div className="glass-card">
        <h3 style={{ fontSize: '18px', marginBottom: '16px' }}>Risk Factors</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <RiskFactor 
            label="Wallet History" 
            value="Good" 
            status="positive"
          />
          <RiskFactor 
            label="Transaction Pattern" 
            value="Normal" 
            status="positive"
          />
          <RiskFactor 
            label="Volume Spike" 
            value="Moderate" 
            status="warning"
          />
          <RiskFactor 
            label="Smart Contract Risk" 
            value="Low" 
            status="positive"
          />
        </div>
      </div>

      {/* Status Card */}
      <div className="glass-card">
        <h3 style={{ fontSize: '18px', marginBottom: '16px' }}>Analysis Status</h3>
        <div style={{ padding: '16px', background: 'rgba(16, 185, 129, 0.1)', borderRadius: '12px', border: '1px solid rgba(16, 185, 129, 0.3)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
            <div style={{ width: '8px', height: '8px', background: '#10b981', borderRadius: '50%' }}></div>
            <span style={{ fontWeight: '600', color: '#10b981' }}>Analysis Complete</span>
          </div>
          <p style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>
            Last updated: {new Date(riskData.timestamp).toLocaleTimeString()}
          </p>
        </div>
      </div>
    </div>
  )
}

function RiskFactor({ 
  label, 
  value, 
  status 
}: { 
  label: string 
  value: string 
  status: 'positive' | 'warning' | 'danger'
}) {
  const colors = {
    positive: '#10b981',
    warning: '#f59e0b',
    danger: '#ef4444'
  }

  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <span style={{ color: 'var(--text-secondary)' }}>{label}</span>
      <span style={{ 
        fontWeight: '600', 
        color: colors[status],
        padding: '4px 12px',
        background: `${colors[status]}20`,
        borderRadius: '8px',
        fontSize: '13px'
      }}>
        {value}
      </span>
    </div>
  )
}
