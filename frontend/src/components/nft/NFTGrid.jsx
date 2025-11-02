import { useEffect, useState } from "react";
import { fetchUserNFTs } from "../../api/userNfts";
export default function NFTGrid({ username, type }) {
  const [items, setItems] = useState([]);
  const [page, setPage] = useState(1);
  const [hasNext, setHasNext] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setItems([]);
    setPage(1);
  }, [username, type]);

  useEffect(() => {
    if (!username) return;
    let cancelled = false;
    setLoading(true);
    fetchUserNFTs(username, type, page, 24).then((d) => {
      if (cancelled) return;
      setItems((prev) => (page === 1 ? d.results : [...prev, ...d.results]));
      setHasNext(Boolean(d.next));
      setLoading(false);
    });
    return () => { cancelled = true; };
  }, [username, type, page]);

  return (
    <div>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
        {items.map((nft) => (
          <div key={nft.id} className="rounded-2xl shadow p-3">
            <img
              src={nft.image_src || "/placeholder-nft.png"}
              alt={nft.name}
              className="rounded-xl w-full h-48 object-cover"
            />
            <div className="mt-2 font-medium">{nft.name}</div>
            {nft.price != null && (
              <div className="text-sm text-gray-500">{nft.price} ETH</div>
            )}
            <div className="text-xs text-gray-400 mt-1">
              owner: {nft.owner} • creator: {nft.creator}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 flex justify-center">
        {hasNext ? (
          <button
            className="px-4 py-2 rounded-xl border"
            onClick={() => setPage((p) => p + 1)}
            disabled={loading}
          >
            {loading ? "Loading..." : "Load more"}
          </button>
        ) : (
          items.length > 0 && <div className="text-gray-500">No more items</div>
        )}
      </div>
    </div>
  );
}

NFTGrid.defaultProps = {
  type: "owned",
};