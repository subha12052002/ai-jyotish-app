/**
 * AI Jyotish — Dashboard Module
 * --------------------------------
 * Responsible only for dashboard presentation.
 *
 * All astrology calculations come from the backend.
 */

(function () {
    "use strict";

    const MODULE_NAME = "AIJyotishDashboard";

    const PLANET_SYMBOLS = {
        Sun: "☉",
        Moon: "☽",
        Mars: "♂",
        Mercury: "☿",
        Jupiter: "♃",
        Venus: "♀",
        Saturn: "♄",
        Rahu: "☊",
        Ketu: "☋"
    };

    const PLANET_CLASSES = {
        Sun: "sun",
        Moon: "moon",
        Mars: "mars",
        Mercury: "mercury",
        Jupiter: "jupiter",
        Venus: "venus",
        Saturn: "saturn",
        Rahu: "rahu",
        Ketu: "ketu"
    };

    function escapeHtml(value) {
        if (value === null || value === undefined) return "";

        return String(value)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function getValue(object, keys, fallback = "—") {
        if (!object || typeof object !== "object") {
            return fallback;
        }

        for (const key of keys) {
            if (
                object[key] !== undefined &&
                object[key] !== null &&
                object[key] !== ""
            ) {
                return object[key];
            }
        }

        return fallback;
    }

    function getPlanetSymbol(planet) {
        return PLANET_SYMBOLS[planet] || "✦";
    }

    function getPlanetClass(planet) {
        return PLANET_CLASSES[planet] || "";
    }

    function getChartValue(chart, keys, fallback = "—") {
        for (const key of keys) {
            const direct = chart?.[key];

            if (
                direct !== undefined &&
                direct !== null &&
                direct !== ""
            ) {
                return direct;
            }

            const nested = chart?.basic?.[key];

            if (
                nested !== undefined &&
                nested !== null &&
                nested !== ""
            ) {
                return nested;
            }

            const analysis = chart?.analysis?.[key];

            if (
                analysis !== undefined &&
                analysis !== null &&
                analysis !== ""
            ) {
                return analysis;
            }
        }

        return fallback;
    }

    function getPlanet(chart, planetName) {
        const planets =
            chart?.planets ||
            chart?.planetary_positions ||
            chart?.planetaryPositions ||
            {};

        if (Array.isArray(planets)) {
            return planets.find(item => {
                const name = getValue(
                    item,
                    ["name", "planet", "body"],
                    ""
                );

                return String(name).toLowerCase() ===
                    planetName.toLowerCase();
            }) || null;
        }

        return planets[planetName] ||
            planets[planetName.toLowerCase()] ||
            null;
    }

    function getPlanetSign(chart, planetName) {
        const planet = getPlanet(chart, planetName);

        if (!planet) return "—";

        return getValue(
            planet,
            ["sign", "rashi", "zodiac", "sign_name"],
            "—"
        );
    }

    function renderUserName(chart) {
        const element = document.getElementById("userName");

        if (!element) return;

        const name = getChartValue(
            chart,
            ["name", "full_name", "fullName"],
            "Seeker"
        );

        element.textContent = name;
    }

    function renderCoreStats(chart) {
        const sunSign = getChartValue(
            chart,
            ["sun_sign", "sunSign", "sun_rashi"],
            getPlanetSign(chart, "Sun")
        );

        const moonSign = getChartValue(
            chart,
            ["moon_sign", "moonSign", "moon_rashi"],
            getPlanetSign(chart, "Moon")
        );

       const ascendantData = chart?.ascendant || {};

const ascendant = getValue(
    ascendantData,
    ["sign", "name"],
    "—"
);

const nakshatraData = chart?.dashas?.nakshatra || {};

const nakshatra = getValue(
    nakshatraData,
    ["name"],
    "—"
);

const nakshatraLord = getValue(
    nakshatraData,
    ["lord"],
    "—"
);

       const dashaData =
    chart?.dashas ||
    chart?.analysis?.dashas ||
    {};

const currentMahadasha =
    dashaData?.current_mahadasha || null;

const dashaLord =
    dashaData?.current_mahadasha_lord ||
    "—";

let dasha = dashaLord;

if (currentMahadasha && typeof currentMahadasha === "object") {
    dasha =
        currentMahadasha.lord ||
        currentMahadasha.name ||
        dashaLord;
}
        const yogaData =
            chart?.yogas ||
            chart?.yoga ||
            chart?.analysis?.yogas ||
            [];

        let yogaCount = 0;

        if (Array.isArray(yogaData)) {
            yogaCount = yogaData.length;
        } else if (yogaData && typeof yogaData === "object") {
            yogaCount = Object.keys(yogaData).length;
        }

       setText("sunSign", sunSign);
setText("moonSign", moonSign);
setText("ascendant", ascendant);
setText("nakshatra", nakshatra);
setText("nakshatraLord", nakshatraLord);
setText("dasha", dasha);
setText("yogaCount", yogaCount);
    }

    function setText(id, value) {
        const element = document.getElementById(id);

        if (!element) return;

        element.textContent =
            value === undefined ||
            value === null ||
            value === ""
                ? "—"
                : value;
    }

    function renderMiniPlanetPanel(chart) {
        const target =
            document.getElementById("dashboardPlanetPreview");

        if (!target) return;

        const planets = [
            "Sun",
            "Moon",
            "Mars",
            "Mercury",
            "Jupiter",
            "Venus",
            "Saturn",
            "Rahu",
            "Ketu"
        ];

        target.innerHTML = `
            <div class="dashboard-planet-grid">
                ${planets.map(planet => {
                    const sign = getPlanetSign(chart, planet);

                    return `
                        <div class="dashboard-planet-item">
                            <div class="dashboard-planet-symbol ${getPlanetClass(
                                planet
                            )}">
                                ${escapeHtml(
                                    getPlanetSymbol(planet)
                                )}
                            </div>

                            <div class="dashboard-planet-info">
                                <strong>
                                    ${escapeHtml(planet)}
                                </strong>

                                <span>
                                    ${escapeHtml(sign)}
                                </span>
                            </div>
                        </div>
                    `;
                }).join("")}
            </div>
        `;
    }

    function renderWelcome(chart) {
        const target =
            document.getElementById("dashboardWelcome");

        if (!target) return;

        const name = getChartValue(
            chart,
            ["name", "full_name", "fullName"],
            "Seeker"
        );

        target.innerHTML = `
            <div class="dashboard-welcome-content">
                <span class="dashboard-welcome-eyebrow">
                    ✦ YOUR VEDIC PROFILE
                </span>

                <h1>
                    Welcome,
                    <span>${escapeHtml(name)}</span>
                </h1>

                <p>
                    Your birth chart is ready. Explore your
                    planetary placements, Nakshatra, Dasha
                    periods and Yogas.
                </p>
            </div>
        `;
    }

    function renderQuickAccess() {
        const target =
            document.getElementById("quickAccess");

        if (!target) return;

        const items = [
            {
                href: "kundli.html",
                icon: "◈",
                title: "Full Kundli",
                text: "Open your complete birth chart"
            },
            {
                href: "birth-form.html",
                icon: "＋",
                title: "New Chart",
                text: "Calculate another birth chart"
            }
        ];

        target.innerHTML = `
            <div class="dashboard-quick-grid">
                ${items.map(item => `
                    <a
                        class="dashboard-quick-card"
                        href="${escapeHtml(item.href)}"
                    >
                        <span class="dashboard-quick-icon">
                            ${escapeHtml(item.icon)}
                        </span>

                        <span class="dashboard-quick-content">
                            <strong>
                                ${escapeHtml(item.title)}
                            </strong>

                            <small>
                                ${escapeHtml(item.text)}
                            </small>
                        </span>

                        <span class="dashboard-quick-arrow">
                            →
                        </span>
                    </a>
                `).join("")}
            </div>
        `;
    }

    function renderChartSummary(chart) {
        const target =
            document.getElementById("chartSummary");

        if (!target) return;

        const birthDate = getChartValue(
            chart,
            ["date", "birth_date", "birthDate"],
            "—"
        );

        const birthTime = getChartValue(
            chart,
            ["time", "birth_time", "birthTime"],
            "—"
        );

        const place = getChartValue(
            chart,
            ["place", "birth_place", "birthPlace"],
            "—"
        );

        target.innerHTML = `
            <div class="dashboard-chart-summary">
                <div class="dashboard-summary-item">
                    <span>Birth Date</span>
                    <strong>
                        ${escapeHtml(birthDate)}
                    </strong>
                </div>

                <div class="dashboard-summary-item">
                    <span>Birth Time</span>
                    <strong>
                        ${escapeHtml(birthTime)}
                    </strong>
                </div>

                <div class="dashboard-summary-item">
                    <span>Birth Place</span>
                    <strong>
                        ${escapeHtml(place)}
                    </strong>
                </div>
            </div>
        `;
    }

    function render(chart) {
        if (!chart) return;

        renderUserName(chart);
        renderWelcome(chart);
        renderCoreStats(chart);
        renderMiniPlanetPanel(chart);
        renderChartSummary(chart);
        renderQuickAccess();
    }

    function init(chart) {
        if (!chart) return;

        render(chart);
    }

    window[MODULE_NAME] = {
        render,
        init,
        renderUserName,
        renderWelcome,
        renderCoreStats,
        renderMiniPlanetPanel,
        renderChartSummary,
        renderQuickAccess
    };
})();