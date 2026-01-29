/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    webpack: (config, { isServer }) => {
        // Fix for MetaMask SDK and WalletConnect trying to import Node/React Native modules
        if (!isServer) {
            config.resolve.fallback = {
                ...config.resolve.fallback,
                '@react-native-async-storage/async-storage': false,
                'pino-pretty': false,
                fs: false,
                net: false,
                tls: false,
            }
        }

        // Suppress specific warnings
        config.ignoreWarnings = [
            { module: /node_modules\/@metamask\/sdk/ },
            { module: /node_modules\/pino/ },
        ]

        return config
    },
}

module.exports = nextConfig
