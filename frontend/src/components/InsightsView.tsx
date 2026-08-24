import { useEffect, useState } from "react"

import {
  getCollectionInsights,
  type CollectionInsights,
} from "../api/client"


function formatPlayedAt(value: string): string {
  const date = new Date(value)

  return new Intl.DateTimeFormat(
    undefined,
    {
      day: "numeric",
      month: "short",
      year: "numeric",
    },
  ).format(date)
}


function InsightsView() {
  const [insights, setInsights] =
    useState<CollectionInsights | null>(null)

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    async function loadInsights() {
      try {
        const result = await getCollectionInsights()
        setInsights(result)
      } catch (err) {
        console.error(err)

        setError(
          "Couldn't load your collection insights.",
        )
      } finally {
        setLoading(false)
      }
    }

    loadInsights()
  }, [])

  if (loading) {
    return (
      <section className="screen insights-screen">
        <p className="eyebrow">Your shelf</p>
        <h1>Crunching the numbers...</h1>
      </section>
    )
  }

  if (error || !insights) {
    return (
      <section className="screen insights-screen">
        <p className="eyebrow">Your shelf</p>
        <h1>Collection insights</h1>

        <p className="error-message">
          {error}
        </p>
      </section>
    )
  }

  return (
    <section className="screen insights-screen">
      <header>
        <p className="eyebrow">Your shelf</p>

        <h1>Collection insights</h1>

        <p className="subtitle">
          A quick look at what's hitting the table.
        </p>
      </header>

      <div className="insights-stat-grid">
        <article className="stat-card">
          <strong>{insights.total_games}</strong>
          <span>Games owned</span>
        </article>

        <article className="stat-card">
          <strong>{insights.total_plays}</strong>
          <span>Recorded plays</span>
        </article>
      </div>

      <div className="insight-feature-list">
        <article className="insight-feature">
          <p className="insight-label">
            Most played
          </p>

          {insights.most_played ? (
            <>
              <h2>
                {insights.most_played.name}
              </h2>

              <p className="insight-detail">
                {insights.most_played.play_count}{" "}
                {insights.most_played.play_count === 1
                  ? "play"
                  : "plays"}
              </p>
            </>
          ) : (
            <p className="insight-empty">
              No plays recorded yet.
            </p>
          )}
        </article>

        <article className="insight-feature">
          <p className="insight-label">
            Last played
          </p>

          {insights.last_played ? (
            <>
              <h2>
                {insights.last_played.name}
              </h2>

              <p className="insight-detail">
                {formatPlayedAt(
                  insights.last_played.played_at,
                )}
              </p>
            </>
          ) : (
            <p className="insight-empty">
              Nothing has hit the table yet.
            </p>
          )}
        </article>
      </div>

      <article className="shelf-callout">
        <strong>
          {insights.never_played_count}
        </strong>

        <div>
          <span>games waiting</span>

          <p>
            Still looking for their next night
            on the table.
          </p>
        </div>
      </article>
    </section>
  )
}

export default InsightsView