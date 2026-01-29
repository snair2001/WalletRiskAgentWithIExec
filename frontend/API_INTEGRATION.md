# API Integration Guide

## 🔗 Real Blockchain Data Integration

The wallet risk monitor now fetches **real data** from blockchain APIs!

## Setup Instructions

### 1. Get Your Free Etherscan API Key

1. Visit [https://etherscan.io](https://etherscan.io)
2. Create a free account
3. Go to [My API Keys](https://etherscan.io/myapikey)
4. Create a new API key
5. Copy your API key

### 2. Configure Environment Variables

Create a `.env.local` file in the frontend directory:

```bash
cd frontend
cp .env.local.example .env.local
```

Edit `.env.local` and add your API key:

```env
NEXT_PUBLIC_ETHERSCAN_API_KEY=your_actual_api_key_here
```

### 3. Restart the Dev Server

```bash
npm run dev
```

## What Data is Fetched

### Portfolio Overview (Real-Time)

| Field | Source | Description |
|-------|--------|-------------|
| **Total Value** | Etherscan + CoinGecko | ETH balance × current ETH price in USD |
| **Wallet Age** | Etherscan | Days since first transaction |
| **Transactions** | Etherscan | Total number of transactions |
| **Last Activity** | Etherscan | Time since last transaction |

## API Endpoints

### GET `/api/portfolio/[address]`

Fetches portfolio data for a wallet address.

**Parameters:**
- `address` - Ethereum wallet address (0x...)

**Response:**
```json
{
  "totalValue": 1234.56,
  "walletAge": 500,
  "transactions": 1250,
  "lastActivity": "2 hours ago"
}
```

**Error Responses:**
- `400` - Invalid wallet address
- `500` - API fetch failed

## Data Sources

### Etherscan API
- **Rate Limit**: 5 calls/second (free tier)
- **Endpoints Used**:
  - `/api?module=account&action=balance` - Get ETH balance
  - `/api?module=account&action=txlist` - Get transaction history

### CoinGecko API
- **Rate Limit**: 10-50 calls/minute (free tier)
- **Endpoint Used**:
  - `/simple/price?ids=ethereum&vs_currencies=usd` - Get ETH price

## Important Notes

### Current Limitations

1. **Only ETH Balance**: Currently calculates value based on ETH only, not ERC-20 tokens
2. **Mainnet Only**: Only supports Ethereum mainnet (not testnets yet)
3. **Rate Limits**: Free tier has rate limits - may need caching for production

### Future Enhancements

To get **complete portfolio value** including tokens:

```typescript
// Add ERC-20 token balance fetching
const tokenListResponse = await fetch(
  `https://api.etherscan.io/api?module=account&action=tokentx&address=${walletAddress}`
)

// Get token prices from CoinGecko
const tokenPrices = await fetch(
  'https://api.coingecko.com/api/v3/simple/token_price/ethereum'
)

// Calculate total value
const totalValue = ethValue + sum(tokenBalances × tokenPrices)
```

## Testing

### Test with Real Wallets

Try these example addresses:

```typescript
// Vitalik's wallet (public)
const testAddress = '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045'

// Or use your own MetaMask address
```

### Verify Data

Compare the data shown in the app with:
- [Etherscan](https://etherscan.io) - Transaction count, wallet age
- [DeBank](https://debank.com) - Portfolio value
- Your MetaMask wallet - ETH balance

## Troubleshooting

### "Failed to fetch portfolio data"

**Causes:**
1. No Etherscan API key configured
2. Invalid wallet address
3. Rate limit exceeded
4. Network error

**Solutions:**
1. Check `.env.local` file exists and has valid API key
2. Ensure wallet address starts with `0x` and is 42 characters
3. Wait a few seconds and retry
4. Check browser console for detailed errors

### Slow Loading

**Optimization:**
```typescript
// Add caching to reduce API calls
const cachedData = localStorage.getItem(`portfolio_${walletAddress}`)
if (cachedData && Date.now() - cache.timestamp < 60000) {
  // Use cached data if less than 1 minute old
  return JSON.parse(cachedData)
}
```

## Production Deployment

For production use:

1. **Get paid API tier** for higher rate limits
2. **Add caching layer** (Redis or similar)
3. **Use Alchemy/Infura** for more reliable blockchain access
4. **Add retry logic** for failed API calls
5. **Monitor API usage** to stay within limits

Enjoy real-time blockchain data! 🚀
