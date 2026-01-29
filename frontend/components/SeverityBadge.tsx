'use client'

import { CheckCircle, AlertCircle, AlertTriangle, Skull } from 'lucide-react'

type SeverityLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'

interface SeverityBadgeProps {
  severity: SeverityLevel
}

export default function SeverityBadge({ severity }: SeverityBadgeProps) {
  const config = {
    LOW: {
      Icon: CheckCircle,
      label: 'Low Risk',
      description: 'Wallet appears safe',
      className: 'low'
    },
    MEDIUM: {
      Icon: AlertCircle,
      label: 'Medium Risk',
      description: 'Exercise caution',
      className: 'medium'
    },
    HIGH: {
      Icon: AlertTriangle,
      label: 'High Risk',
      description: 'Confirmation required',
      className: 'high'
    },
    CRITICAL: {
      Icon: Skull,
      label: 'Critical Risk',
      description: 'Wallet paused',
      className: 'critical'
    }
  }

  const { Icon, label, description, className } = config[severity]

  return (
    <div className={`severity-badge ${className}`}>
      <div className="badge-icon">
        <Icon size={24} />
      </div>
      <div className="badge-content">
        <div className="badge-label">{label}</div>
        <div className="badge-description">{description}</div>
      </div>
    </div>
  )
}
