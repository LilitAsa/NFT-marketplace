import { useEffect, useState } from "react";
import { api } from "../../api/client";

export default function ProDashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError]   = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadStats() {
      try {
        const { data } = await api.get("accounts/pro/stats/");
        if (!cancelled) {
          setStats(data);
        }
      } catch (e) {
        if (!cancelled) setError(`Не удалось загрузить статистику: ${e.message}`);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    loadStats();
    return () => { cancelled = true; };
  }, []);

  if (loading) return <div className="p-6">Загрузка Pro Dashboard…</div>;
  if (error)   return <div className="p-6 text-red-400">{error}</div>;

  return (
    <div className="p-6 pt-30 max-w-4xl">
      <h1 className="text-2xl font-semibold">Pro Dashboard</h1>
      <p className="text-gray-400 mt-2">Инструменты для роли Pro</p>

      <div className="grid gap-4 mt-6 md:grid-cols-3">
        <div className="glass-card p-4">
          <div className="text-sm text-gray-400">Всего продаж</div>
          <div className="text-2xl font-bold text-blue-400">
            {stats.total_sales}
          </div>
        </div>
        <div className="glass-card p-4">
          <div className="text-sm text-gray-400">Активных листингов</div>
          <div className="text-2xl font-bold text-purple-400">
            {stats.nfts_listed}
          </div>
        </div>
      </div>

      <div className="mt-6">
        <h2 className="text-xl font-semibold mb-4">Недавние продажи</h2>
        {stats.recent_sales.length === 0 ? (
          <p className="text-gray-400">Нет недавних продаж.</p>
        ) : (
          <table className="w-full table-auto border-collapse">
            <thead>
              <tr>
                <th className="border-b border-gray-700 pb-2 text-left">NFT</th>
                <th className="border-b border-gray-700 pb-2 text-left">Цена</th>
                <th className="border-b border-gray-700 pb-2 text-left">Дата</th>
              </tr>
            </thead>
            <tbody>
              {stats.recent_sales.map((sale) => (
                <tr key={sale.id} className="hover:bg-gray-800">
                  <td className="py-2">{sale.nft_name}</td>
                  <td className="py-2">{sale.price} ETH</td>
                  <td className="py-2">{new Date(sale.date).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}