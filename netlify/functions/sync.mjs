import { getStore } from "@netlify/blobs";

const store = getStore({ name: "security-manager-sync", consistency: "strong" });

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "no-store"
    }
  });
}

function isValidKey(value) {
  return typeof value === "string" && /^[a-f0-9]{64}$/.test(value);
}

export default async req => {
  if (req.method !== "POST" && req.method !== "PUT") {
    return json({ error: "Method not allowed" }, 405);
  }

  const payload = await req.json().catch(() => null);
  const key = payload?.key;

  if (!isValidKey(key)) {
    return json({ error: "Invalid sync key" }, 400);
  }

  if (req.method === "POST") {
    const entry = await store.get(`sync/${key}`, {
      type: "json",
      consistency: "strong"
    });

    if (!entry) {
      return json({ error: "Not found" }, 404);
    }

    return json(entry);
  }

  const record = {
    payload: payload?.payload || null,
    updatedAt: new Date().toISOString(),
    device: String(payload?.device || "browser")
  };

  await store.setJSON(`sync/${key}`, record);
  return json(record);
};

export const config = {
  path: "/api/sync"
};
