/**
 * AI Jyotish — Yoga Module
 * --------------------------------
 * Displays calculated Vedic astrology Yogas.
 *
 * IMPORTANT:
 * Yoga calculations are NOT performed here.
 * The backend remains the source of truth.
 */

(function () {
    "use strict";

    const MODULE_NAME = "AIJyotishYogas";

    const CATEGORY_META = {
        raja: {
            label: "Raja Yoga",
            icon: "♛",
            description: "Power, authority and achievement"
        },
        dhana: {
            label: "Dhana Yoga",
            icon: "₹",
            description: "Wealth and financial potential"
        },
        dharma: {
            label: "Dharma Yoga",
            icon: "☸",
            description: "Purpose, fortune and higher principles"
        },
        viparita: {
            label: "Viparita Raja Yoga",
            icon: "↟",
            description: "Growth through challenges"
        },
        mahapurusha: {
            label: "Mahapurusha Yoga",
            icon: "✦",
            description: "Exceptional planetary strength"
        },
        lunar: {
            label: "Lunar Yoga",
            icon: "☽",
            description: "Mind, emotions and mental patterns"
        },
        solar: {
            label: "Solar Yoga",
            icon: "☉",
            description: "Vitality, confidence and authority"
        },
        other: {
            label: "Special Yoga",
            icon: "✧",
            description: "Special planetary combination"
        }
    };

    function escapeHtml(value) {
        if (value === null || value === undefined) {
            return "";
        }

        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function getValue(object, keys, fallback = null) {
        if (!object || typeof object !== "object") {
            return fallback;
        }

        for (const key of keys) {
            if (
                Object.prototype.hasOwnProperty.call(object, key) &&
                object[key] !== null &&
                object[key] !== undefined
            ) {
                return object[key];
            }
        }

        return fallback;
    }

    function normalizeCategory(value) {
        if (!value) {
            return "other";
        }

        const text = String(value)
            .toLowerCase()
            .replace(/[_-]/g, " ")
            .trim();

        if (
            text.includes("raja") ||
            text.includes("raj") ||
            text.includes("royal")
        ) {
            return "raja";
        }

        if (
            text.includes("dhana") ||
            text.includes("wealth")
        ) {
            return "dhana";
        }

        if (
            text.includes("dharma") ||
            text.includes("fortune")
        ) {
            return "dharma";
        }

        if (
            text.includes("viparita") ||
            text.includes("vipreet")
        ) {
            return "viparita";
        }

        if (text.includes("mahapurusha")) {
            return "mahapurusha";
        }

        if (
            text.includes("lunar") ||
            text.includes("chandra") ||
            text.includes("moon")
        ) {
            return "lunar";
        }

        if (
            text.includes("solar") ||
            text.includes("surya") ||
            text.includes("sun")
        ) {
            return "solar";
        }

        return "other";
    }

    function normalizeStrength(value) {
        if (value === null || value === undefined) {
            return null;
        }

        if (typeof value === "number") {
            return Math.max(0, Math.min(100, value));
        }

        const text = String(value).toLowerCase().trim();

        if (text.includes("very strong")) {
            return 95;
        }

        if (text.includes("strong")) {
            return 80;
        }

        if (text.includes("moderate")) {
            return 60;
        }

        if (text.includes("weak")) {
            return 30;
        }

        const number = parseFloat(text);

        if (Number.isFinite(number)) {
            return Math.max(0, Math.min(100, number));
        }

        return null;
    }

    function getStrengthLabel(value) {
        const score = normalizeStrength(value);

        if (score === null) {
            return "Calculated";
        }

        if (score >= 80) {
            return "Strong";
        }

        if (score >= 60) {
            return "Moderate";
        }

        if (score >= 40) {
            return "Mild";
        }

        return "Weak";
    }

    function normalizeYoga(item) {
        if (!item) {
            return null;
        }

        if (typeof item === "string") {
            return {
                name: item,
                category: normalizeCategory(item),
                description: "",
                effects: "",
                strength: null,
                planets: [],
                houses: [],
                active: true
            };
        }

        const name = getValue(item, [
            "name",
            "yoga",
            "yoga_name",
            "yogaName",
            "title"
        ], "Unnamed Yoga");

        const category = normalizeCategory(
            getValue(item, [
                "category",
                "type",
                "group",
                "classification"
            ], name)
        );

        const description = getValue(item, [
            "description",
            "meaning",
            "interpretation",
            "details"
        ], "");

        const effects = getValue(item, [
            "effects",
            "result",
            "results",
            "prediction",
            "impact"
        ], "");

        const strength = getValue(item, [
            "strength",
            "power",
            "score",
            "percentage"
        ], null);

        let planets = getValue(item, [
            "planets",
            "planetary_involvement",
            "planetaryInvolvement"
        ], []);

        if (!Array.isArray(planets)) {
            planets = planets
                ? String(planets)
                    .split(",")
                    .map(value => value.trim())
                    .filter(Boolean)
                : [];
        }

        let houses = getValue(item, [
            "houses",
            "house_involvement",
            "houseInvolvement"
        ], []);

        if (!Array.isArray(houses)) {
            houses = houses
                ? String(houses)
                    .split(",")
                    .map(value => value.trim())
                    .filter(Boolean)
                : [];
        }

        return {
            ...item,
            name,
            category,
            description,
            effects,
            strength,
            planets,
            houses,
            active:
                item.active !== false &&
                item.present !== false &&
                item.exists !== false
        };
    }

    function extractYogas(chart) {
        if (!chart) {
            return [];
        }

        const raw =
            chart.yogas ||
            chart.yoga ||
            chart.analysis?.yogas ||
            chart.analysis?.yoga ||
            [];

        if (Array.isArray(raw)) {
            return raw
                .map(normalizeYoga)
                .filter(Boolean)
                .filter(yoga => yoga.active);
        }

        if (typeof raw === "object") {
            const possibleList =
                raw.list ||
                raw.results ||
                raw.detected ||
                raw.present ||
                raw.yogas ||
                [];

            if (Array.isArray(possibleList)) {
                return possibleList
                    .map(normalizeYoga)
                    .filter(Boolean)
                    .filter(yoga => yoga.active);
            }

            return Object.entries(raw)
                .filter(([, value]) => value)
                .map(([name, value]) => {
                    if (typeof value === "object") {
                        return normalizeYoga({
                            ...value,
                            name
                        });
                    }

                    return normalizeYoga({
                        name,
                        description: String(value)
                    });
                })
                .filter(Boolean)
                .filter(yoga => yoga.active);
        }

        return [];
    }

    function getCategoryMeta(category) {
        return CATEGORY_META[category] || CATEGORY_META.other;
    }

    function renderYogaCount(chart, target) {
        if (!target) {
            return;
        }

        const yogas = extractYogas(chart);

        target.textContent = String(yogas.length);
    }

    function renderSummary(chart, target) {
        if (!target) {
            return;
        }

        const yogas = extractYogas(chart);

        if (!yogas.length) {
            target.innerHTML = `
                <div class="yoga-summary-empty">
                    <span class="yoga-summary-icon">✧</span>
                    <div>
                        <strong>No major Yogas detected</strong>
                        <p>
                            No qualifying planetary combinations
                            were returned by the calculation engine.
                        </p>
                    </div>
                </div>
            `;
            return;
        }

        const categories = {};

        yogas.forEach(yoga => {
            categories[yoga.category] =
                (categories[yoga.category] || 0) + 1;
        });

        target.innerHTML = `
            <div class="yoga-summary">
                <div class="yoga-summary-total">
                    <span class="yoga-summary-number">
                        ${yogas.length}
                    </span>

                    <div>
                        <span class="yoga-summary-label">
                            Detected Yogas
                        </span>

                        <p>
                            Important planetary combinations
                            identified in your birth chart.
                        </p>
                    </div>
                </div>

                <div class="yoga-summary-categories">
                    ${Object.entries(categories)
                        .map(([category, count]) => {
                            const meta = getCategoryMeta(category);

                            return `
                                <div class="yoga-category-mini">
                                    <span>${escapeHtml(meta.icon)}</span>
                                    <div>
                                        <strong>
                                            ${escapeHtml(meta.label)}
                                        </strong>
                                        <small>
                                            ${count} detected
                                        </small>
                                    </div>
                                </div>
                            `;
                        })
                        .join("")}
                </div>
            </div>
        `;
    }

    function renderYogaList(chart, target) {
        if (!target) {
            return;
        }

        const yogas = extractYogas(chart);

        if (!yogas.length) {
            target.innerHTML = `
                <div class="yoga-empty">
                    <div class="yoga-empty-icon">✧</div>
                    <h3>No Major Yogas Found</h3>
                    <p>
                        The current birth chart does not contain
                        any qualifying Yogas returned by the
                        astrology calculation engine.
                    </p>
                </div>
            `;
            return;
        }

        target.innerHTML = `
            <div class="yoga-grid">
                ${yogas.map((yoga, index) => {
                    const meta = getCategoryMeta(yoga.category);
                    const strength = normalizeStrength(yoga.strength);

                    return `
                        <article
                            class="yoga-card"
                            data-yoga-index="${index}"
                        >
                            <div class="yoga-card-header">
                                <div class="yoga-card-icon">
                                    ${escapeHtml(meta.icon)}
                                </div>

                                <div class="yoga-card-title">
                                    <span class="yoga-card-category">
                                        ${escapeHtml(meta.label)}
                                    </span>

                                    <h3>
                                        ${escapeHtml(yoga.name)}
                                    </h3>
                                </div>

                                <span class="yoga-status">
                                    Present
                                </span>
                            </div>

                            ${
                                yoga.description
                                    ? `
                                        <p class="yoga-description">
                                            ${escapeHtml(
                                                yoga.description
                                            )}
                                        </p>
                                    `
                                    : ""
                            }

                            ${
                                yoga.effects
                                    ? `
                                        <div class="yoga-effects">
                                            <span>✦</span>
                                            <div>
                                                <strong>Influence</strong>
                                                <p>
                                                    ${escapeHtml(
                                                        yoga.effects
                                                    )}
                                                </p>
                                            </div>
                                        </div>
                                    `
                                    : ""
                            }

                            ${
                                yoga.planets.length
                                    ? `
                                        <div class="yoga-detail-row">
                                            <span>Planets</span>
                                            <div class="yoga-tags">
                                                ${yoga.planets
                                                    .map(
                                                        planet => `
                                                            <span class="yoga-tag">
                                                                ${escapeHtml(
                                                                    planet
                                                                )}
                                                            </span>
                                                        `
                                                    )
                                                    .join("")}
                                            </div>
                                        </div>
                                    `
                                    : ""
                            }

                            ${
                                yoga.houses.length
                                    ? `
                                        <div class="yoga-detail-row">
                                            <span>Houses</span>
                                            <div class="yoga-tags">
                                                ${yoga.houses
                                                    .map(
                                                        house => `
                                                            <span class="yoga-tag">
                                                                ${escapeHtml(
                                                                    house
                                                                )}
                                                            </span>
                                                        `
                                                    )
                                                    .join("")}
                                            </div>
                                        </div>
                                    `
                                    : ""
                            }

                            ${
                                strength !== null
                                    ? `
                                        <div class="yoga-strength">
                                            <div class="yoga-strength-label">
                                                <span>
                                                    Strength
                                                </span>
                                                <strong>
                                                    ${getStrengthLabel(
                                                        strength
                                                    )}
                                                </strong>
                                            </div>

                                            <div class="yoga-strength-track">
                                                <div
                                                    class="yoga-strength-bar"
                                                    style="width:${strength}%"
                                                ></div>
                                            </div>
                                        </div>
                                    `
                                    : ""
                            }
                        </article>
                    `;
                }).join("")}
            </div>
        `;
    }

    function render(chart) {
        if (!chart) {
            return;
        }

        const list =
            document.getElementById("yogaList");

        const summary =
            document.getElementById("yogaSummary");

        const count =
            document.getElementById("yogaCount");

        renderYogaList(chart, list);
        renderSummary(chart, summary);
        renderYogaCount(chart, count);
    }

    function getYogas(chart) {
        return extractYogas(chart);
    }

    function hasYogas(chart) {
        return extractYogas(chart).length > 0;
    }

    window[MODULE_NAME] = {
        render,
        renderYogaList,
        renderSummary,
        renderYogaCount,
        extractYogas,
        getYogas,
        hasYogas,
        normalizeYoga
    };
})();