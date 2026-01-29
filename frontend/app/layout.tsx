import type { Metadata } from 'next'
import './globals.css'
import { Web3Provider } from '@/config/web3'

export const metadata: Metadata = {
  title: 'Wallet Risk Monitor',
  description: 'Privacy-preserving wallet risk analysis powered by iExec',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <Web3Provider>
          {children}
        </Web3Provider>
      </body>
    </html>
  )
}
