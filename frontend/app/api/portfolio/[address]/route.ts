import { NextRequest, NextResponse } from 'next/server'

interface PortfolioData {
    totalValue: number
    walletAge: number
    transactions: number
    lastActivity: string
}

export async function GET(
    request: NextRequest,
    { params }: { params: { address: string } }
) {
    const walletAddress = params.address

    if (!walletAddress || !walletAddress.match(/^0x[a-fA-F0-9]{40}$/)) {
        return NextResponse.json(
            { error: 'Invalid wallet address' },
            { status: 400 }
        )
    }

    try {
        // Detect network from query parameter (defaults to mainnet)
        const { searchParams } = new URL(request.url)
        const network = searchParams.get('network') || 'mainnet'

        // Configure API endpoints based on network
        const etherscanApiKey = process.env.NEXT_PUBLIC_ETHERSCAN_API_KEY || 'YourApiKeyToken'
        const baseUrl = network === 'sepolia'
            ? 'https://api-sepolia.etherscan.io/v2/api'
            : 'https://api.etherscan.io/v2/api'

        // 1. Get ETH balance
        const balanceResponse = await fetch(
            `${baseUrl}?module=account&action=balance&address=${walletAddress}&tag=latest&apikey=${etherscanApiKey}`
        )
        const balanceData = await balanceResponse.json()
        const ethBalance = balanceData.status === '1'
            ? parseFloat(balanceData.result) / 1e18
            : 0

        // 2. Get ETH price from CoinGecko (only for mainnet, testnet ETH has no value)
        let ethPrice = 0
        if (network === 'mainnet') {
            const priceResponse = await fetch(
                'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd'
            )
            const priceData = await priceResponse.json()
            ethPrice = priceData.ethereum?.usd || 0
        }

        // Calculate total value (0 for testnet)
        const totalValue = ethBalance * ethPrice

        // 3. Get transaction history for wallet age and last activity
        const txResponse = await fetch(
            `${baseUrl}?module=account&action=txlist&address=${walletAddress}&startblock=0&endblock=99999999&page=1&offset=10000&sort=asc&apikey=${etherscanApiKey}`
        )
        const txData = await txResponse.json()

        let walletAge = 0
        let transactions = 0
        let lastActivity = 'Never'

        if (txData.status === '1' && txData.result.length > 0) {
            // Wallet age (days since first transaction)
            const firstTxTimestamp = parseInt(txData.result[0].timeStamp) * 1000
            walletAge = Math.floor((Date.now() - firstTxTimestamp) / (1000 * 60 * 60 * 24))

            // Total transactions
            transactions = txData.result.length

            // Last activity
            const lastTxTimestamp = parseInt(txData.result[txData.result.length - 1].timeStamp) * 1000
            lastActivity = formatTimeAgo(lastTxTimestamp)
        }

        const portfolioData: PortfolioData = {
            totalValue: Math.round(totalValue * 100) / 100,
            walletAge,
            transactions,
            lastActivity,
        }

        return NextResponse.json(portfolioData)
    } catch (error) {
        console.error('Error fetching portfolio data:', error)
        return NextResponse.json(
            { error: 'Failed to fetch portfolio data' },
            { status: 500 }
        )
    }
}

function formatTimeAgo(timestamp: number): string {
    const seconds = Math.floor((Date.now() - timestamp) / 1000)

    if (seconds < 60) return 'Just now'
    if (seconds < 3600) return `${Math.floor(seconds / 60)} minutes ago`
    if (seconds < 86400) return `${Math.floor(seconds / 3600)} hours ago`
    if (seconds < 2592000) return `${Math.floor(seconds / 86400)} days ago`
    if (seconds < 31536000) return `${Math.floor(seconds / 2592000)} months ago`
    return `${Math.floor(seconds / 31536000)} years ago`
}
