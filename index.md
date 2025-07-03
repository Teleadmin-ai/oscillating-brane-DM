---
layout: home
title: Home
---

# Welcome to Oscillating Brane Cosmology

## The Universe as a Vibrating Cosmic Membrane

Imagine the universe not as a vast void punctuated by stars, but as the skin of an infinitely extended cosmic drum. This elastic membrane—our four-dimensional reality—floats in an ocean of hidden dimensions.

<div class="hero-section">
  <div class="key-predictions">
    <h3>🌌 Key Predictions</h3>
    <table>
      <tr>
        <td><strong>Brane tension</strong></td>
        <td>τ₀ = 7.0 × 10¹⁹ J/m²</td>
      </tr>
      <tr>
        <td><strong>Oscillation period</strong></td>
        <td>T = 2.0 ± 0.3 Gyr</td>
      </tr>
      <tr>
        <td><strong>MOND acceleration</strong></td>
        <td>a₀ = 1.1 × 10⁻¹⁰ m/s²</td>
      </tr>
      <tr>
        <td><strong>S₈ suppression</strong></td>
        <td>-5.2%</td>
      </tr>
      <tr>
        <td><strong>Bayesian evidence</strong></td>
        <td>Δln K = 3.33 ± 0.24</td>
      </tr>
    </table>
  </div>
</div>

## Revolutionary Insights

Our theory presents a paradigm shift in understanding cosmic dynamics:

- **Black holes** are not destructive chasms but tension pegs, anchor points where the membrane folds
- **Dark matter** is the invisible bow that vibrates this giant harp
- **Dark energy** emerges naturally from membrane oscillations
- **Modified gravity** appears at cosmic scales without new particles

## Recent Posts

{% for post in site.posts limit:3 %}
  <article class="post-preview">
    <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
    <time>{{ post.date | date: "%B %d, %Y" }}</time>
    <p>{{ post.excerpt | strip_html | truncate: 200 }}</p>
  </article>
{% endfor %}

<style>
.hero-section {
  margin: 2em 0;
  padding: 2em;
  background: #f8f9fa;
  border-radius: 8px;
}

.key-predictions table {
  width: 100%;
  border-collapse: collapse;
}

.key-predictions td {
  padding: 0.5em;
  border-bottom: 1px solid #dee2e6;
}

.post-preview {
  margin: 2em 0;
  padding-bottom: 1em;
  border-bottom: 1px solid #eee;
}

.post-preview h3 {
  margin-bottom: 0.3em;
}

.post-preview time {
  color: #666;
  font-size: 0.9em;
}
</style>