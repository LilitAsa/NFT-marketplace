import { api } from "./client";

export async function fetchUserNFTs(username, type = "owned", page = 1, pageSize = 24) {
  const { data } = await api.get(`/users/${encodeURIComponent(username)}/nfts`, {
    params: { type, page, page_size: pageSize },
  });
  return data; // { count, next, previous, results: [...] }
}