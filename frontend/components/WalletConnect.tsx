'use client'

import React, { useEffect, useState } from 'react'
import { useAccount, useConnect, useDisconnect } from 'wagmi'

interface WalletConnectProps {
  onConnect: (address: string) => void
  onDisconnect: () => void
  isConnected: boolean
  address: string | null
}

export default function WalletConnect({ 
  onConnect, 
  onDisconnect, 
  isConnected: _isConnected, 
  address: _address 
}: WalletConnectProps) {
  
  const [mounted, setMounted] = useState(false)
  
  // Use wagmi hooks for real wallet connection
  const { address, isConnected } = useAccount()
  const { connect, connectors } = useConnect()
  const { disconnect } = useDisconnect()

  // Ensure component only renders on client
  useEffect(() => {
    setMounted(true)
  }, [])

  // Update parent component when connection changes
  useEffect(() => {
    if (mounted && isConnected && address) {
      onConnect(address)
    } else if (mounted && !isConnected) {
      onDisconnect()
    }
  }, [mounted, isConnected, address, onConnect, onDisconnect])

  const handleConnect = () => {
    // Connect with the first available connector (MetaMask/injected wallet)
    const injectedConnector = connectors.find(c => c.type === 'injected')
    if (injectedConnector) {
      connect({ connector: injectedConnector })
    }
  }

  const handleDisconnect = () => {
    disconnect()
    onDisconnect()
  }

  const formatAddress = (addr: string) => {
    return `${addr.slice(0, 6)}...${addr.slice(-4)}`
  }

  // Prevent rendering until mounted on client to avoid hydration mismatch
  if (!mounted) {
    return (
      <div className="wallet-connect">
        <div className="connect-options">
          <button className="btn-primary" disabled>
            🦊 Connect MetaMask
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="wallet-connect">
      {!isConnected ? (
        <div className="connect-options">
          <button 
            onClick={handleConnect}
            className="btn-primary"
          >
            🦊 Connect MetaMask
          </button>
        </div>
      ) : (
        <div className="wallet-info">
          <div className="address-badge">
            <div className="green-dot"></div>
            <span>{address && formatAddress(address)}</span>
          </div>
          <button onClick={handleDisconnect} className="btn-disconnect">
            Disconnect
          </button>
        </div>
      )}
    </div>
  )
}
