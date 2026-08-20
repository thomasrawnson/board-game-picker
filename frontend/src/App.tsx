import { useState } from "react"
import { getMessage } from "./api/client"

function App() {
  const [message, setMessage] = useState("")
  const [loading, setLoading] = useState(false)

  async function handlePickGame() {
    setLoading(true)

    try {
      const result = await getMessage()
      setMessage(result)
    } catch (error) {
      setMessage("Something went wrong. Please try again.")
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main>
      <h1>🎲 Board Game Picker</h1>

      <p>What are we playing tonight?</p>

      <button onClick={handlePickGame} disabled={loading}>
        {loading ? "Finding a game..." : "🎲 Pick a Game"}
      </button>

      {message && (
        <p>{message}</p>
      )}
    </main>
  )
}

export default App