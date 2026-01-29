# MetaMask Integration Guide

## ✅ Real Wallet Connection Enabled!

The application now connects to **real MetaMask wallets** instead of using mock addresses.

## How to Use

### 1. Install MetaMask
If you don't have MetaMask installed:
- Visit [metamask.io](https://metamask.io)
- Install the browser extension
- Create or import a wallet

### 2. Connect Your Wallet
1. Open http://localhost:3000
2. Click "🦊 Connect MetaMask"
3. MetaMask popup will appear
4. Select the account you want to connect
5. Click "Connect" in MetaMask

### 3. Switch Accounts
To test with different accounts:

**Method 1: Disconnect and Reconnect**
1. Click "Disconnect" button in the app
2. Click "Connect MetaMask" again
3. In MetaMask popup, click "Not you?" or the account selector
4. Choose a different account

**Method 2: Switch in MetaMask**
1. Keep the wallet connected
2. Open MetaMask extension
3. Click on your account icon
4. Select a different account
5. The app will automatically update to the new address

### 4. View in Wallets Monitor
Every wallet you connect will be automatically:
- Added to the "Wallets Monitor" tab
- Tracked with last seen timestamp
- Displayed with risk analysis data
- Stored in localStorage for persistence

## Technical Details

### Supported Networks
- Ethereum Mainnet
- Sepolia Testnet
- Polygon

### Libraries Used
- **wagmi**: React hooks for Ethereum
- **viem**: TypeScript-first Web3 library
- **@tanstack/react-query**: Data fetching and caching

### Features
- ✅ Real MetaMask integration
- ✅ Account switching detection
- ✅ Network detection
- ✅ Auto-reconnection on page reload
- ✅ Disconnect functionality
- ✅ Address formatting and display

## Troubleshooting

### MetaMask Not Popping Up?
- Make sure MetaMask extension is installed and unlocked
- Check that you're using Chrome, Firefox, or Brave browser
- Try refreshing the page

### Wrong Network?
- The app supports Mainnet, Sepolia, and Polygon
- Switch networks in MetaMask if needed

### Connection Not Working?
- Clear browser cache and localStorage
- Make sure MetaMask is not locked
- Try disconnecting and reconnecting

## Testing Multiple Accounts

1. **Create test accounts in MetaMask:**
   - Open MetaMask
   - Click account icon
   - Click "Create Account"
   - Name it (e.g., "Test Account 2")

2. **Test the flow:**
   - Connect with Account 1 → Check Wallets Monitor
   - Disconnect
   - Connect with Account 2 → Check Wallets Monitor
   - Both accounts should now appear in the monitor!

3. **Switch between accounts:**
   - While connected, open MetaMask
   - Select different account
   - App updates automatically
   - New account is tracked

Enjoy real Web3 wallet connections! 🎉
