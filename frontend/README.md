# Wallet Risk Monitor - Frontend

Modern, privacy-preserving wallet risk analysis dashboard powered by iExec Secure Compute.

## Features

- 🔗 **Wallet Connection**: Easy MetaMask integration
- 📊 **Risk Dashboard**: Real-time risk scoring with confidence levels
- 🎨 **Severity Badges**: Color-coded risk indicators (LOW, MEDIUM, HIGH, CRITICAL)
- 📜 **Audit History**: Complete analysis timeline with filtering
- 👥 **Wallets Monitor**: Track all connected wallets with their risk profiles
- 🌙 **Dark Theme**: Beautiful glassmorphism design

## Getting Started

### Install Dependencies

```bash
npm install
```

### Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
npm run build
npm start
```

## Tech Stack

- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Lucide React** - Modern icons
- **CSS Modules** - Scoped styling with glassmorphism

## Project Structure

```
frontend/
├── app/
│   ├── globals.css       # Global styles and design system
│   ├── layout.tsx        # Root layout
│   └── page.tsx          # Main application page
├── components/
│   ├── WalletConnect.tsx   # Wallet connection component
│   ├── RiskDashboard.tsx   # Risk visualization dashboard
│   ├── SeverityBadge.tsx   # Risk level indicators
│   ├── AuditHistory.tsx    # Historical analysis view
│   └── WalletsMonitor.tsx  # Monitor all wallets
└── package.json
```

## Features in Detail

### Wallet Connection
- Simulated MetaMask connection (ready for wagmi integration)
- Address display with formatting
- Connection status indicator
- Auto-saves to Wallets Monitor

### Risk Dashboard
- Current risk score display
- Portfolio overview
- Risk factor breakdown
- Real-time status updates

### Audit History
- Timeline of all analyses
- Filter by severity level
- Statistics dashboard
- Transaction links to Etherscan

### Wallets Monitor (NEW!)
- View all wallets ever connected
- Grid layout with wallet cards
- Sort by: Most Recent, Highest Risk, Most Analyzed
- Filter by severity level
- Statistics: Total wallets, High risk count, Low risk count, Avg analyses
- Each wallet shows:
  - Address with optional nickname
  - Current risk score with trend indicator
  - Severity badge
  - Confidence level
  - Total analysis count
  - Last seen timestamp
- Stored in localStorage for persistence

## Customization

The design system uses CSS variables defined in `app/globals.css`:

```css
:root {
    --risk-low: #10b981;
    --risk-medium: #f59e0b;
    --risk-high: #ef4444;
    --risk-critical: #7f1d1d;
    --primary: #3b82f6;
    --secondary: #8b5cf6;
}
```

## Next Steps

1. **Web3 Integration**: Connect to real wallets with wagmi/viem
2. **Backend API**: Connect to analysis engine and smart contracts
3. **Real-time Events**: Listen for contract events
4. **Chart Integration**: Add Chart.js for trend visualization
5. **Deployment**: Deploy to Vercel or similar platform

## License

MIT
