'use client'

import { useState } from 'react'
import WalletConnect from '@/components/WalletConnect'
import RiskDashboard from '@/components/RiskDashboard'
import AuditHistory from '@/components/AuditHistory'
import WalletsMonitor from '@/components/WalletsMonitor'

export default function Home() {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'history' | 'monitor'>('dashboard')
  const [walletAddress, setWalletAddress] = useState<string | null>(null)
  const [isConnected, setIsConnected] = useState(false)

  const handleConnect = (address: string) => {
    setWalletAddress(address)
    setIsConnected(true)
    
    // Store connected wallet
    const stored = localStorage.getItem('monitoredWallets')
    const wallets = stored ? JSON.parse(stored) : []
    
    // Add to monitored wallets if not already there
    if (!wallets.find((w: any) => w.address === address)) {
      wallets.push({
        address,
        lastSeen: Date.now(),
        currentRiskScore: 42,
        severity: 'MEDIUM',
        confidence: 87,
        totalAnalyses: 1,
        averageRiskScore: 42,
        trend: 'stable'
      })
      localStorage.setItem('monitoredWallets', JSON.stringify(wallets))
    }
  }

  const handleDisconnect = () => {
    setWalletAddress(null)
    setIsConnected(false)
  }

  return (
    <div className="app-container">
      <header className="app-header glass-card">
        <div className="header-left">
          <h1>🛡️ Wallet Risk Monitor</h1>
          <p>Powered by iExec Secure Compute</p>
        </div>
        <WalletConnect 
          onConnect={handleConnect}
          onDisconnect={handleDisconnect}
          isConnected={isConnected}
          address={walletAddress}
        />
      </header>

      {isConnected && walletAddress ? (
        <>
          <nav className="app-nav">
            <button 
              onClick={() => setActiveTab('dashboard')}
              className={activeTab === 'dashboard' ? 'active' : ''}
            >
              📊 Dashboard
            </button>
            <button 
              onClick={() => setActiveTab('history')}
              className={activeTab === 'history' ? 'active' : ''}
            >
              📜 Audit History
            </button>
            <button 
              onClick={() => setActiveTab('monitor')}
              className={activeTab === 'monitor' ? 'active' : ''}
            >
              👥 Wallets Monitor
            </button>
          </nav>

          <main className="app-main">
            {activeTab === 'dashboard' && <RiskDashboard walletAddress={walletAddress} />}
            {activeTab === 'history' && <AuditHistory walletAddress={walletAddress} />}
            {activeTab === 'monitor' && <WalletsMonitor />}
          </main>
        </>
      ) : (
        <div className="connect-prompt glass-card">
          <h2>Connect Your Wallet</h2>
          <p>Connect your wallet to view risk analysis and audit history</p>
        </div>
      )}
    </div>
  )
}
