import { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import NFTGrid from "../components/nft/NFTGrid";
import { useNavigate } from "react-router-dom";




export default function ProfilePage() {
  const { username } = useParams();
  const [profile, setProfile] = useState(null);
  const [tab, setTab] = useState("overview"); // overview | collected | created
  const navigate = useNavigate();


  useEffect(() => {
    const access = localStorage.getItem("access");
    if (!access) {
      navigate("/login", { replace: true });
      return; // не дергаем /me
    }
    const me = localStorage.getItem("username") || "anonymous";
    setProfile({
      username: username || me,
      display_name: username || me,
      bio: "",
      avatar: "",
      wallet_address: "",
      nfts_collected: 0,
      nfts_created: 0,
      followers: 0,
    });
  }, [username, navigate]);

  const isOwner = useMemo(() => {
    const me = localStorage.getItem("username");
    return me && profile && me === profile.username;
  }, [profile]);

  console.log(isOwner,'isOwner');

  if (!profile) return <div className="p-6">Loading…</div>;

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="flex items-start gap-6">
        <img src={profile.avatar || "/placeholder-avatar.png"} alt="avatar"
             className="w-32 h-32 rounded-2xl object-cover shadow" />
        <div className="flex-1">
          <h1 className="text-2xl font-semibold">{profile.display_name || profile.username}</h1>
          <p className="text-sm text-gray-500 break-all">{profile.wallet_address || "No wallet linked"}</p>
          <div className="mt-3 flex gap-4 text-sm">
            <span><b>{profile.nfts_collected}</b> Collected</span>
            <span><b>{profile.nfts_created}</b> Created</span>
            <span><b>{profile.followers}</b> Followers</span>
          </div>
          {profile.bio && <div className="mt-2 text-gray-700 whitespace-pre-wrap">{profile.bio}</div>}
        </div>
      </div>

      <div className="mt-8 border-b flex gap-6 overflow-x-auto">
        {["overview","collected","created"].map(k => (
          <button key={k}
                  className={`py-2 border-b-2 -mb-px ${tab===k ? "border-black" : "border-transparent text-gray-500"}`}
                  onClick={() => setTab(k)}>
            {k[0].toUpperCase()+k.slice(1)}
          </button>
        ))}
      </div>

      <div className="mt-6">
        {(tab==="overview" || tab==="collected") && <NFTGrid username={profile.username} type="owned" />}
        {tab==="created" && <NFTGrid username={profile.username} type="created" />}
      </div>
    </div>
  );
}
