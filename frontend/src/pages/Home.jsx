import { useState } from "react";
import { Link } from "react-router-dom";
import Button from "../components/common/button/Button";

export default function HomePage() {
  const [mode, setMode] = useState("collector");

  return (
    <div className="dark-bg min-h-screen">
      {/* Header */}
      <header className="glass-card mx-4 mt-4 p-4 neon-border">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <h1 className="text-2xl font-bold gradient-text">NFT Marketplace</h1>
            <div className="mode-switcher flex">
              <button
                onClick={() => setMode("collector")}
                className={`px-4 py-2 rounded-lg text-sm font-medium mode-button ${
                  mode === "collector" ? "mode-active" : "text-gray-400"
                }`}
              >
                Collector
              </button>
              <button
                onClick={() => setMode("pro")}
                className={`px-4 py-2 rounded-lg text-sm font-medium mode-button ${
                  mode === "pro" ? "mode-active" : "text-gray-400"
                }`}
              >
                Pro
              </button>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <button className="text-gray-400 hover:text-white transition-colors">
              Wallet
            </button>
            <Link 
              to="/login" 
              className="btn-modern px-6 py-2 rounded-lg text-sm font-medium"
            >
              Login
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="text-center py-20 px-4">
        <h2 className="text-5xl font-bold gradient-text mb-6">
          Discover & Trade NFTs
        </h2>
        <p className="text-xl text-gray-400 mb-8 max-w-2xl mx-auto">
          Explore the world's largest digital marketplace for crypto collectibles and non-fungible tokens
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button className="btn-modern px-8 py-4 rounded-lg text-lg font-medium">
            Explore Collections
          </Button>
          <Button className="glass-card px-8 py-4 rounded-lg text-lg font-medium text-white hover:bg-opacity-80 transition-all">
            Create NFT
          </Button>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <h3 className="text-3xl font-bold text-center text-white mb-12">
            Marketplace Statistics
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="stats-card p-6 text-center">
              <div className="text-3xl font-bold text-blue-400 mb-2">1.2M+</div>
              <div className="text-gray-400">NFTs Available</div>
            </div>
            <div className="stats-card p-6 text-center">
              <div className="text-3xl font-bold text-purple-400 mb-2">500K+</div>
              <div className="text-gray-400">Active Users</div>
            </div>
            <div className="stats-card p-6 text-center">
              <div className="text-3xl font-bold text-green-400 mb-2">$2.5B+</div>
              <div className="text-gray-400">Total Volume</div>
            </div>
            <div className="stats-card p-6 text-center">
              <div className="text-3xl font-bold text-orange-400 mb-2">10K+</div>
              <div className="text-gray-400">Collections</div>
            </div>
          </div>
        </div>
      </section>

      {/* Featured Collections */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <h3 className="text-3xl font-bold text-center text-white mb-12">
            Featured Collections
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              { name: "Bored Ape Yacht Club", floor: "12.5 ETH", volume: "2.1K ETH" },
              { name: "CryptoPunks", floor: "45.2 ETH", volume: "5.8K ETH" },
              { name: "Azuki", floor: "3.8 ETH", volume: "1.2K ETH" }
            ].map((collection, index) => (
              <div key={index} className="glass-card p-6 neon-border">
                <div className="w-full h-48 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg mb-4"></div>
                <h4 className="text-xl font-bold text-white mb-2">{collection.name}</h4>
                <div className="flex justify-between text-sm text-gray-400">
                  <span>Floor: {collection.floor}</span>
                  <span>Volume: {collection.volume}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="glass-card mx-4 mb-4 p-6 neon-border">
        <div className="text-center text-gray-400">
          <p>&copy; 2025 NFT Marketplace. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
