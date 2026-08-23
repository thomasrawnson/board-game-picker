export interface Game {
  bgg_id: number
  name: string
  year_published: number | null
  min_players: number | null
  max_players: number | null
  min_play_time: number | null
  max_play_time: number | null
  complexity: number | null
  rating: number | null
  owned: boolean
  image_url: string | null
  thumbnail_url: string | null
}

export interface PickerMatch {
  game: Game
  score: number
  reasons: string[]
}

export interface PickerCriteria {
  players: number
  maxPlayTime?: number
}

const API_BASE_URL = "http://127.0.0.1:8000"

export async function getPickerMatches(
  criteria: PickerCriteria,
): Promise<PickerMatch[]> {
  const params = new URLSearchParams({
    players: criteria.players.toString(),
    limit: "20",
  })

  if (criteria.maxPlayTime !== undefined) {
    params.set(
      "max_play_time",
      criteria.maxPlayTime.toString(),
    )
  }

  const response = await fetch(
    `${API_BASE_URL}/picker?${params.toString()}`,
  )

  if (!response.ok) {
    throw new Error(
      `Picker request failed: ${response.status}`,
    )
  }

  return response.json()
}