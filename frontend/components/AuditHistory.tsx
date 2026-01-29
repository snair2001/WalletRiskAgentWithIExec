'use client'

import { useEffect, useState } from 'react'
import SeverityBadge from './SeverityBadge'

interface AuditEvent {
  id: string
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'
  riskScore: number
  confidence: number
  timestamp: number
  reasoning: string
  txHash?: string
}

interface AuditHistoryProps {
  walletAddress: string
}

export default function AuditHistory({ walletAddress }: AuditHistoryProps) {
  const [history, setHistory] = useState<AuditEvent[]>([])
  const [filter, setFilter] = useState<'ALL' | 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'>('ALL')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate fetching audit history
    setTimeout(() => {
      const mockHistory: AuditEvent[] = [
        {
          id: '1',
          severity: 'MEDIUM',
          riskScore: 42,
          confidence: 87,
          timestamp: Date.now() - 3600000,
          reasoning: 'Wallet shows moderate transaction volume with normal patterns',
          txHash: '0x1234567890abcdef'
        },
        {
          id: '2',
          severity: 'LOW',
          riskScore: 18,
          confidence: 92,
          timestamp: Date.now() - 86400000,
          reasoning: 'Wallet activity is normal with established history',
          txHash: '0xabcdef1234567890'
        },
        {
          id: '3',
          severity: 'HIGH',
          riskScore: 68,
          confidence: 78,
          timestamp: Date.now() - 172800000,
          reasoning: 'Unusual transaction spike detected. User confirmation required.',
          txHash: '0xfedcba0987654321'
        }
      ]
      setHistory(mockHistory)
      setLoading(false)
    }, 800)
  }, [walletAddress])

  const filteredHistory = filter === 'ALL' 
    ? history 
    : history.filter(e => e.severity === filter)

  const getAvgRiskScore = () => {
    if (history.length === 0) return 0
    return Math.round(history.reduce((sum, e) => sum + e.riskScore, 0) / history.length)
  }

  if (loading) {
    return (
      <div className="loading-spinner">
        <div className="spinner"></div>
      </div>
    )
  }

  return (
    <div>
      {/* Header with Filters */}
      <div className="glass-card" style={{ marginBottom: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
          <h2 style={{ fontSize: '24px', fontWeight: '700' }}>Audit History</h2>
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            {(['ALL', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'] as const).map(f => (
              <button
                key={f}
                onClick={() => setFilter(f)}
                style={{
                  padding: '8px 16px',
                  borderRadius: '8px',
                  border: 'none',
                  background: filter === f ? 'linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%)' : 'rgba(255, 255, 255, 0.05)',
                  color: filter === f ? 'white' : 'var(--text-secondary)',
                  cursor: 'pointer',
                  fontWeight: '600',
                  fontSize: '13px',
                  transition: 'all 0.2s ease'
                }}
              >
                {f}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Statistics */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '24px' }}>
        <StatCard label="Total Analyses" value={history.length.toString()} />
        <StatCard label="Avg Risk Score" value={`${getAvgRiskScore()}/100`} />
        <StatCard label="High Risk Events" value={history.filter(e => e.severity === 'HIGH').length.toString()} />
        <StatCard label="Critical Events" value={history.filter(e => e.severity === 'CRITICAL').length.toString()} />
      </div>

      {/* Timeline */}
      <div>
        {filteredHistory.length > 0 ? (
          filteredHistory.map((event) => (
            <TimelineEvent key={event.id} event={event} />
          ))
        ) : (
          <div className="glass-card" style={{ textAlign: 'center', padding: '60px 20px' }}>
            <p style={{ color: 'var(--text-secondary)' }}>No events found for this filter</p>
          </div>
        )}
      </div>
    </div>
  )
}

function StatCard({ label, value }: { label: string, value: string }) {
  return (
    <div className="glass-card" style={{ textAlign: 'center' }}>
      <p style={{ color: 'var(--text-secondary)', fontSize: '14px', marginBottom: '8px' }}>{label}</p>
      <p style={{ fontSize: '32px', fontWeight: '700', background: 'linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>{value}</p>
    </div>
  )
}

function TimelineEvent({ event }: { event: AuditEvent }) {
  const formatDateTime = (timestamp: number) => {
    const date = new Date(timestamp)
    return date.toLocaleString()
  }

  return (
    <div className="glass-card" style={{ marginBottom: '16px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px', flexWrap: 'wrap', gap: '12px' }}>
        <div>
          <p style={{ color: 'var(--text-secondary)', fontSize: '13px', marginBottom: '4px' }}>
            {formatDateTime(event.timestamp)}
          </p>
          <SeverityBadge severity={event.severity} />
        </div>
        <div style={{ textAlign: 'right' }}>
          <p style={{ fontSize: '32px', fontWeight: '700', lineHeight: '1' }}>
            {event.riskScore}
            <span style={{ fontSize: '16px', color: 'var(--text-secondary)' }}>/100</span>
          </p>
          <p style={{ color: 'var(--text-secondary)', fontSize: '13px', marginTop: '4px' }}>
            Confidence: {event.confidence}%
          </p>
        </div>
      </div>

      <p style={{ color: 'var(--text)', marginBottom: '12px', fontSize: '14px' }}>
        {event.reasoning}
      </p>


    </div>
  )
}
