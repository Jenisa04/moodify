from utils.lastfm import lf_tracks
tracks = lf_tracks("scared", api_key="70b00dd7ae7257714f3a69f1c662e70b", limit=5)
for t in tracks:
    print(t["name"], "—", t["artist"])
