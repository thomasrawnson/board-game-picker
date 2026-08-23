import { useState } from "react"
import {
  getPickerMatches,
  recordPlay,
  type PickerMatch,
} from "./api/client"

import "./App.css"

type Step = "players" | "time" | "reveal"

const playerOptions = [2, 3, 4, 5, 6, 7]

const timeOptions = [
  {
    label: "Quick",
    description: "under 30 min",
    value: 30,
  },
  {
    label: "Standard",
    description: "up to 60 min",
    value: 60,
  },
  {
    label: "Deep dive",
    description: "up to 120 min",
    value: 120,
  },
  {
    label: "All night",
    description: "no limit",
    value: undefined,
  },
]

function App() {
  const [step, setStep] = useState<Step>("players")
  const [players, setPlayers] = useState<number | null>(null)
  const [maxPlayTime, setMaxPlayTime] = useState<
    number | undefined
  >(undefined)

  const [matches, setMatches] = useState<PickerMatch[]>([])
  const [matchIndex, setMatchIndex] = useState(0)

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const [savingPlay, setSavingPlay] = useState(false)
  const [playRecorded, setPlayRecorded] = useState(false)
  const [playError, setPlayError] = useState("")

  async function revealGame() {
    if (players === null) {
      return
    }

    setLoading(true)
    setError("")

    try {
      const results = await getPickerMatches({
        players,
        maxPlayTime,
      })

      if (results.length === 0) {
        setError(
          "No games matched those choices. Try allowing more time.",
        )
        return
      }

      setMatches(results)
      setMatchIndex(0)
      setStep("reveal")
    } catch (err) {
      console.error(err)

      setError(
        "Couldn't reach the Board Game Picker API.",
      )
    } finally {
      setLoading(false)
    }
  }

  async function handlePlayThis() {
    if (!match || players === null) {
      return
    }

    setSavingPlay(true)
    setPlayError("")

    try {
      await recordPlay(
        match.game.bgg_id,
        players,
      )

      setPlayRecorded(true)
    } catch (err) {
      console.error(err)

      setPlayError(
        "Couldn't record this play. Please try again.",
      )
    } finally {
      setSavingPlay(false)
    }
  }


function tryAnother() {
  if (matches.length === 0) {
    return
  }

  setPlayRecorded(false)
  setPlayError("")

  setMatchIndex(
    (current) => (current + 1) % matches.length,
  )
}

  const match = matches[matchIndex]

  return (
    <main className="app-shell">
      <section className="phone">
        <div className="progress-dots">
          <span
            className={
              step === "players" ? "dot active" : "dot"
            }
          />
          <span
            className={
              step === "time" ? "dot active" : "dot"
            }
          />
          <span
            className={
              step === "reveal" ? "dot active" : "dot"
            }
          />
        </div>

        {step === "players" && (
          <section className="screen">
            <header>
              <p className="eyebrow">Game night</p>

              <h1>Who's playing?</h1>

              <p className="subtitle">
                Pick a number, we'll do the rest.
              </p>
            </header>

            <div className="player-grid">
              {playerOptions.map((option) => (
                <button
                  key={option}
                  className={
                    players === option
                      ? "player-chip selected"
                      : "player-chip"
                  }
                  onClick={() => setPlayers(option)}
                >
                  <strong>
                    {option === 7 ? "7+" : option}
                  </strong>

                  <span>Players</span>
                </button>
              ))}
            </div>

            <button
              className="primary-button"
              disabled={players === null}
              onClick={() => setStep("time")}
            >
              Continue
            </button>
          </section>
        )}

        {step === "time" && (
          <section className="screen">
            <header>
              <p className="eyebrow">Game night</p>

              <h1>How long you got?</h1>

              <p className="subtitle">
                We'll only show games that fit.
              </p>
            </header>

            <div className="time-list">
              {timeOptions.map((option) => {
                const selected =
                  maxPlayTime === option.value

                return (
                  <button
                    key={option.label}
                    className={
                      selected
                        ? "time-option selected"
                        : "time-option"
                    }
                    onClick={() =>
                      setMaxPlayTime(option.value)
                    }
                  >
                    <strong>{option.label}</strong>

                    <span>{option.description}</span>
                  </button>
                )
              })}
            </div>

            {error && (
              <p className="error-message">{error}</p>
            )}

            <button
              className="primary-button"
              onClick={revealGame}
              disabled={loading}
            >
              {loading
                ? "Searching the shelf..."
                : "Reveal a game"}
            </button>

            <button
              className="ghost-button"
              onClick={() => setStep("players")}
            >
              Back
            </button>
          </section>
        )}

        {step === "reveal" && match && (
          <section className="screen reveal-screen">
            <div
              className="game-card"
              key={match.game.bgg_id}
              >
              <div className="game-image-wrap">
                {match.game.image_url ||
                match.game.thumbnail_url ? (
                  <img
                    className="game-image"
                    src={
                      match.game.image_url ??
                      match.game.thumbnail_url ??
                      ""
                    }
                    alt={match.game.name}
                  />
                ) : (
                  <div className="image-placeholder">
                    ?
                  </div>
                )}

                <div className="match-score">
                  <strong>{match.score}</strong>
                  <span>Match</span>
                </div>
              </div>

              <h2>{match.game.name}</h2>

              <div className="game-meta">
                {match.game.min_players !== null &&
                  match.game.max_players !== null && (
                    <span>
                      {match.game.min_players}–
                      {match.game.max_players} players
                    </span>
                  )}

                {match.game.max_play_time !== null && (
                  <span>
                    {match.game.min_play_time ?? "?"}–
                    {match.game.max_play_time} min
                  </span>
                )}
              </div>
            </div>

            <div className="match-reasons">
              {match.reasons.map((reason) => (
                <p key={reason}>✓ {reason}</p>
              ))}
            </div>

            <p className="result-count">
              {matchIndex + 1} of {matches.length} matches
            </p>

            <div className="reveal-actions">
              <button
                className="secondary-button"
                onClick={tryAnother}
              >
                Try another
              </button>

              <button
                className="primary-button"
                onClick={handlePlayThis}
                disabled={savingPlay || playRecorded}
              >
                {savingPlay
                  ? "Recording..."
                  : playRecorded
                    ? "Play recorded"
                    : "Play this"}
              </button>
            </div>

            <button
              className="ghost-button"
              onClick={() => setStep("players")}
            >
              Start over
            </button>
          </section>
        )}
      </section>
    </main>
  )
}

export default App