const API_BASE_URL = "http://127.0.0.1:8000"

export async function getMessage(): Promise<string> {
  const response = await fetch(`${API_BASE_URL}/api/message`)

  if (!response.ok) {
    throw new Error("Failed to contact Board Game Picker API")
  }

  const data = await response.json()

  return data.message
}