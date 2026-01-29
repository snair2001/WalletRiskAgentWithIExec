'use client'

import { useEffect, useState } from 'react'
import SeverityBadge from './SeverityBadge'
import { TrendingUp, TrendingDown, Activity, Clock } from 'lucide-react'

interface WalletData {
  address: string
  lastSeen: number
  currentRiskScore: number
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'
  confidence: number
  totalAnalyses: number
  averageRiskScore: number
  trend: 'up' | 'down' | 'stable'
  nickname?: string
}

export default function WalletsMonitor() {
  const [wallets, setWallets] = useState<WalletData[]>([])
  const [sortBy, setSortBy] = useState<'recent' | 'risk' | 'analyses'>('recent')
  const [filterSeverity, setFilterSeverity] = useState<'ALL' | 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'>('ALL')

  useEffect(() => {
    // Load monitored wallets from localStorage or API
    loadMonitoredWallets()
  }, [])

  const loadMonitoredWallets = () => {
    // Load only wallets that user has actually connected from localStorage
    const stored = localStorage.getItem('monitoredWallets')
    if (stored) {
      try {
        setWallets(JSON.parse(stored))
      } catch (error) {
        console.error('Failed to load monitored wallets:', error)
        setWallets([])
      }
    } else {
      // No wallets connected yet - empty state
      setWallets([])
    }
  }

  const formatAddress = (address: string) => {
    return `${address.slice(0, 6)}...${address.slice(-4)}`
  }

  const formatTimeAgo = (timestamp: number) => {
    const seconds = Math.floor((Date.now() - timestamp) / 1000)
    
    if (seconds < 60) return 'Just now'
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`
    return `${Math.floor(seconds / 86400)}d ago`
  }

  const sortedWallets = [...wallets].sort((a, b) => {
    switch (sortBy) {
      case 'recent':
        return b.lastSeen - a.lastSeen
      case 'risk':
        return b.currentRiskScore - a.currentRiskScore
      case 'analyses':
        return b.totalAnalyses - a.totalAnalyses
      default:
        return 0
    }
  })

  const filteredWallets = filterSeverity === 'ALL'
    ? sortedWallets
    : sortedWallets.filter(w => w.severity === filterSeverity)

  return (
    <div>
      {/* Header with Stats */}
      <div className="glass-card" style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '24px', fontWeight: '700', marginBottom: '24px' }}>
          📊 Wallets Monitor
        </h2>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '24px' }}>
          <StatCard 
            icon={<Activity size={20} />}
            label="Total Wallets" 
            value={wallets.length.toString()} 
          />
          <StatCard 
            icon={<TrendingUp size={20} />}
            label="High Risk" 
            value={wallets.filter(w => w.severity === 'HIGH' || w.severity === 'CRITICAL').length.toString()} 
            color="var(--risk-high)"
          />
          <StatCard 
            icon={<TrendingDown size={20} />}
            label="Low Risk" 
            value={wallets.filter(w => w.severity === 'LOW').length.toString()} 
            color="var(--risk-low)"
          />
          <StatCard 
            icon={<Clock size={20} />}
            label="Avg Analyses" 
            value={Math.round(wallets.reduce((sum, w) => sum + w.totalAnalyses, 0) / wallets.length || 0).toString()} 
          />
        </div>

        {/* Filters */}
        <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', alignItems: 'center' }}>
          <div>
            <label style={{ fontSize: '13px', color: 'var(--text-secondary)', marginRight: '8px' }}>Sort by:</label>
            <select 
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              style={{
                padding: '8px 16px',
                borderRadius: '8px',
                border: '1px solid var(--glass-border)',
                background: 'var(--glass-bg)',
                color: 'var(--text)',
                cursor: 'pointer',
                fontSize: '14px'
              }}
            >
              <option value="recent">Most Recent</option>
              <option value="risk">Highest Risk</option>
              <option value="analyses">Most Analyzed</option>
            </select>
          </div>

          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            {(['ALL', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'] as const).map(f => (
              <button
                key={f}
                onClick={() => setFilterSeverity(f)}
                style={{
                  padding: '6px 12px',
                  borderRadius: '8px',
                  border: 'none',
                  background: filterSeverity === f ? 'linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%)' : 'rgba(255, 255, 255, 0.05)',
                  color: filterSeverity === f ? 'white' : 'var(--text-secondary)',
                  cursor: 'pointer',
                  fontWeight: '600',
                  fontSize: '12px',
                  transition: 'all 0.2s ease'
                }}
              >
                {f}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Wallets Grid */}
      {filteredWallets.length > 0 ? (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))', gap: '16px' }}>
          {filteredWallets.map((wallet) => (
            <WalletCard key={wallet.address} wallet={wallet} />
          ))}
        </div>
      ) : (
        <div className="glass-card" style={{ textAlign: 'center', padding: '60px 20px' }}>
          <h3 style={{ marginBottom: '12px' }}>
            {wallets.length === 0 ? '👛 No Wallets Connected Yet' : 'No wallets match this filter'}
          </h3>
          <p style={{ color: 'var(--text-secondary)' }}>
            {wallets.length === 0 
              ? 'Connect a wallet to start tracking its risk analysis history' 
              : 'Try adjusting your filters to see more wallets'}
          </p>
        </div>
      )}
    </div>
  )
}

function StatCard({ 
  icon, 
  label, 
  value, 
  color 
}: { 
  icon: React.ReactNode
  label: string
  value: string
  color?: string
}) {
  return (
    <div style={{
      padding: '16px',
      background: 'rgba(255, 255, 255, 0.03)',
      borderRadius: '12px',
      border: '1px solid var(--glass-border)'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px', color: color || 'var(--primary)' }}>
        {icon}
        <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>{label}</span>
      </div>
      <p style={{ fontSize: '28px', fontWeight: '700', color: color || 'var(--text)' }}>{value}</p>
    </div>
  )
}

function WalletCard({ wallet }: { wallet: WalletData }) {
  const formatAddress = (address: string) => {
    return `${address.slice(0, 6)}...${address.slice(-4)}`
  }

  const formatTimeAgo = (timestamp: number) => {
    const seconds = Math.floor((Date.now() - timestamp) / 1000)
    
    if (seconds < 60) return 'Just now'
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`
    return `${Math.floor(seconds / 86400)}d ago`
  }

  const getTrendIcon = () => {
    if (wallet.trend === 'up') return <TrendingUp size={16} color="var(--risk-high)" />
    if (wallet.trend === 'down') return <TrendingDown size={16} color="var(--risk-low)" />
    return <Activity size={16} color="var(--text-secondary)" />
  }

  return (
    <div className="glass-card" style={{ cursor: 'pointer', transition: 'all 0.2s ease' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
        <div style={{ flex: 1 }}>
          {wallet.nickname && (
            <p style={{ fontSize: '14px', fontWeight: '600', marginBottom: '4px' }}>
              {wallet.nickname}
            </p>
          )}
          <p style={{ 
            fontFamily: "'Monaco', monospace", 
            fontSize: '13px', 
            color: 'var(--text-secondary)' 
          }}>
            {formatAddress(wallet.address)}
          </p>
          <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginTop: '4px' }}>
            Last seen: {formatTimeAgo(wallet.lastSeen)}
          </p>
        </div>
        
        {/* Risk Score */}
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: '32px', fontWeight: '700', lineHeight: '1' }}>
            {wallet.currentRiskScore}
            <span style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>/100</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '4px', justifyContent: 'flex-end', marginTop: '4px' }}>
            {getTrendIcon()}
            <span style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>
              Avg: {wallet.averageRiskScore}
            </span>
          </div>
        </div>
      </div>

      {/* Severity Badge */}
      <div style={{ marginBottom: '16px' }}>
        <SeverityBadge severity={wallet.severity} />
      </div>

      {/* Stats */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '12px',
        padding: '12px',
        background: 'rgba(255, 255, 255, 0.02)',
        borderRadius: '8px'
      }}>
        <div>
          <p style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Confidence</p>
          <p style={{ fontSize: '18px', fontWeight: '600' }}>{wallet.confidence}%</p>
        </div>
        <div>
          <p style={{ fontSize: '12px', color: 'var(--text-secondary)' }}>Analyses</p>
          <p style={{ fontSize: '18px', fontWeight: '600' }}>{wallet.totalAnalyses}</p>
        </div>
      </div>

      {/* Action Button */}
      <button
        style={{
          width: '100%',
          marginTop: '12px',
          padding: '10px',
          background: 'rgba(59, 130, 246, 0.1)',
          border: '1px solid rgba(59, 130, 246, 0.3)',
          borderRadius: '8px',
          color: 'var(--primary)',
          cursor: 'pointer',
          fontWeight: '600',
          fontSize: '13px',
          transition: 'all 0.2s ease'
        }}
        onMouseOver={(e) => {
          e.currentTarget.style.background = 'rgba(59, 130, 246, 0.2)'
        }}
        onMouseOut={(e) => {
          e.currentTarget.style.background = 'rgba(59, 130, 246, 0.1)'
        }}
      >
        View Details →
      </button>
    </div>
  )
}
